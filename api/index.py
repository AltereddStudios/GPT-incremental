
import os
import sys
import pty
import fcntl
import struct
import termios
import asyncio
import subprocess
import json
import select

from fastapi import FastAPI, WebSocket
from fastapi.websockets import WebSocketDisconnect
from fastapi.staticfiles import StaticFiles

app = FastAPI()

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_DIR = os.path.join(ROOT, "public")
GAME_PATH = os.path.join(ROOT, "game.py")


@app.get("/health")
def health():
    return {"status": "running"}


@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()

    master, slave = pty.openpty()

    fcntl.ioctl(
        slave,
        termios.TIOCSWINSZ,
        struct.pack("HHHH", 24, 80, 0, 0)
    )

    env = os.environ.copy()
    env["TERM"] = "xterm-256color"

    process = subprocess.Popen(
        [sys.executable, GAME_PATH],
        stdin=slave,
        stdout=slave,
        stderr=slave,
        cwd=ROOT,
        env=env
    )

    os.close(slave)

    async def send_output():
        while True:
            try:
                ready, _, _ = await asyncio.to_thread(
                    select.select,
                    [master],
                    [],
                    [],
                    0.2
                )

                if not ready:
                    if process.poll() is not None:
                        return
                    continue

                output = await asyncio.to_thread(
                    os.read,
                    master,
                    4096
                )

                if not output:
                    return

                await websocket.send_bytes(output)

            except (OSError, WebSocketDisconnect, RuntimeError):
                return

    async def receive_input():
        while process.poll() is None:
            try:
                message = await websocket.receive()

                if message["type"] == "websocket.disconnect":
                    return

                if message.get("bytes") is not None:
                    await asyncio.to_thread(
                        os.write,
                        master,
                        message["bytes"]
                    )

                elif message.get("text") is not None:
                    try:
                        data = json.loads(message["text"])

                        if data.get("type") == "resize":
                            cols = max(
                                1,
                                min(int(data["cols"]), 500)
                            )

                            rows = max(
                                1,
                                min(int(data["rows"]), 500)
                            )

                            fcntl.ioctl(
                                master,
                                termios.TIOCSWINSZ,
                                struct.pack("HHHH", rows, cols, 0, 0)
                            )

                    except (
                        ValueError,
                        KeyError,
                        TypeError,
                        json.JSONDecodeError
                    ):
                        pass

            except (WebSocketDisconnect, OSError, RuntimeError):
                return

    output_task = asyncio.create_task(send_output())
    input_task = asyncio.create_task(receive_input())

    try:
        await asyncio.wait(
            [output_task, input_task],
            return_when=asyncio.FIRST_COMPLETED
        )

    finally:
        if process.poll() is None:
            process.terminate()

        await asyncio.to_thread(process.wait)

        for task in [output_task, input_task]:
            if not task.done():
                task.cancel()

        await asyncio.gather(
            output_task,
            input_task,
            return_exceptions=True
        )

        os.close(master)

    if process.poll() is not None:
        try:
            await websocket.close(code=1000)
        except Exception:
            pass


# Serve the website after registering the WebSocket route.
app.mount(
    "/",
    StaticFiles(directory=PUBLIC_DIR, html=True),
    name="public"
)
