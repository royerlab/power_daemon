from pathlib import Path

PORT = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A5069RR4-if00-port0"
PIN = "d:2:o"
SOCKET_ADDRESS = "/tmp/royerlab_power_daemon.sock"
SOCKET_ADDRESS = "/tmp/royerlab_power_daemon.sock"
DAEMON_SCRIPT = Path(__file__).parent / "daemon.py"