
const isMobile =
    navigator.userAgentData?.mobile ??
    (
        /Android|iPhone|iPad|iPod|Mobile|Tablet/i.test(navigator.userAgent) ||
        (
            navigator.maxTouchPoints > 1 &&
            /Macintosh/.test(navigator.userAgent)
        )
    );

const terminalContainer = document.getElementById("terminal-container");
const mobileMessage = document.getElementById("mobile-message");

if (isMobile) {
    terminalContainer.style.display = "none";
    mobileMessage.style.display = "flex";
} else {

    const terminal = new Terminal({
        cursorBlink: true,
        cursorStyle: "block",
        fontFamily: "monospace",
        fontSize: 14,
        allowTransparency: false,

        theme: {
            background: "#1e1e2e",
            foreground: "#cdd6f4",
            cursor: "#f5e0dc",
            cursorAccent: "#1e1e2e",
            selectionBackground: "#585b70",

            black: "#45475a",
            red: "#f38ba8",
            green: "#a6e3a1",
            yellow: "#f9e2af",
            blue: "#89b4fa",
            magenta: "#f5c2e7",
            cyan: "#94e2d5",
            white: "#bac2de",

            brightBlack: "#585b70",
            brightRed: "#f38ba8",
            brightGreen: "#a6e3a1",
            brightYellow: "#f9e2af",
            brightBlue: "#89b4fa",
            brightMagenta: "#f5c2e7",
            brightCyan: "#94e2d5",
            brightWhite: "#a6adc8"
        }
    });

    const fitAddon = new FitAddon.FitAddon();

    terminal.loadAddon(fitAddon);

    terminal.open(document.getElementById("terminal"));

    terminal.element.style.backgroundColor = "#1e1e2e";

    fitAddon.fit();

    terminal.focus();

    // WebSocket connection

    let socket;
    let reconnectAttempts = 0;
    const maxReconnectAttempts = 5;
    let reconnectTimer = null;
    let manuallyClosed = false;

    function connect() {
        if (manuallyClosed) return;

        terminal.write("\r\nConnecting to server...\r\n");

        const protocol =
            window.location.protocol === "https:" ? "wss:" : "ws:";

        socket = new WebSocket(
            `${protocol}//${window.location.host}/ws`
        );

        socket.binaryType = "arraybuffer";

        socket.onopen = () => {
            reconnectAttempts = 0;

            terminal.write("\r\nConnected.\r\n");

            resizeTerminal();
            terminal.focus();
        };

        socket.onmessage = (event) => {
            terminal.write(new Uint8Array(event.data));
        };

        socket.onerror = () => {
            terminal.write("\r\nConnection error.\r\n");
        };

        socket.onclose = (event) => {
            if (manuallyClosed) return;

            if (event.code === 1000) {
                terminal.write("\r\nGame session ended.\r\n");
                return;
            }

            if (reconnectAttempts < maxReconnectAttempts) {
                reconnectAttempts++;

                const delay = Math.min(
                    1000 * Math.pow(2, reconnectAttempts - 1),
                    10000
                );

                terminal.write(
                    `\r\nConnection lost. Reconnecting (${reconnectAttempts}/${maxReconnectAttempts})...\r\n`
                );

                reconnectTimer = setTimeout(connect, delay);
            } else {
                terminal.write(
                    "\r\nUnable to reconnect. Please refresh the page.\r\n"
                );
            }
        };
    }

    // terminal resize

    function resizeTerminal() {
        fitAddon.fit();

        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({
                type: "resize",
                cols: terminal.cols,
                rows: terminal.rows
            }));
        }
    }

    // input

    terminal.onData((data) => {
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(new TextEncoder().encode(data));
        }
    });

    // focusing

    document.addEventListener("click", () => {
        terminal.focus();
    });

    // Browser resizing

    window.addEventListener("resize", resizeTerminal);

    // Initial connection

    connect();

    // Cleanup

    window.addEventListener("beforeunload", () => {
        manuallyClosed = true;

        if (reconnectTimer) {
            clearTimeout(reconnectTimer);
        }

        if (socket) {
            socket.close();
        }
    });
}
