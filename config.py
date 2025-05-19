from pathlib import Path
import platform
import pyfirmata2

IS_WINDOWS = platform.system() == "Windows"
if IS_WINDOWS:
    SOCKET_ADDRESS = ("127.0.0.1", 65432)  # TCP socket as tuple (host, port)
    PORT = "COM1"
else:
    SOCKET_ADDRESS = "/tmp/royerlab_power_daemon.sock"  # Unix domain socket path
    PORT = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A5069RR4-if00-port0"
PIN = "d:2:o"

DAEMON_SCRIPT = Path(__file__).parent / "daemon.py"