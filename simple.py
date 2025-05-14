# This is a simple example of how to control the arduino board - however, it is slow, about 7s per
# invocation because the board is not always connected. The daemon.py script amortizes the connection
# time by keeping the connection open and using a socket to communicate with the CLI.

import argparse
import pyfirmata2

PORT = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A5069RR4-if00-port0"
PIN = "d:2:o"

def main():
    parser = argparse.ArgumentParser(description="Control power state.")
    parser.add_argument("state", choices=["on", "off"], help="Specify 'on' to power on or 'off' to power off.")
    args = parser.parse_args()

    if args.state == "on":
        print("Powering on...")
    elif args.state == "off":
        print("Powering off...")
    
    board = pyfirmata2.Arduino(PORT)
    pin = board.get_pin(PIN)
    pin.write(args.state == "on")

if __name__ == "__main__":
    main()
