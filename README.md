# Power Control System

This is some simple software to control a relay-switched power bar ((https://a.co/d/0LyXXbR)) using an Arduino Nano running standard firmata.
This system allows us to control and reset microscope hardware from our acquisition program.

## Components

### 1. `board_daemon.py`
- Initializes the Arduino Nano and manages its state. The initialization is slow - (5s). The daemon amortizes this time cost at the beginning.
- Sends logic signals to the power bar to control its state.
- Listens for commands via a Unix socket (`/tmp/board_daemon.sock`).
- Supported commands:
  - `on`: Powers on the power bar.
  - `off`: Powers off the power bar.
  - `status`: Queries the current state of the power bar.

### 2. `main.py`
- Provides a command-line interface to interact with the daemon (meaning that the board is already initialized, and the commands are ~instant).
- Automatically starts the daemon if it is not running.
- Supported actions:
  - `on`: Sends a command to power on the power bar.
  - `off`: Sends a command to power off the power bar.
  - `status`: Queries the current state of the power bar.
  - `kill`: Stops the daemon process.
  - `relaunch`: Restarts the daemon process.

### Starting the Daemon
The daemon is automatically started by the `main.py` script if it is not already running.

### Command-Line Interface
Run the `main.py` script with one of the following actions:

```bash
python3 main.py [action]
```

#### Actions:
- `on`: Powers on the power bar.
- `off`: Powers off the power bar.
- `status`: Queries the current state of the power bar.
- `kill`: Stops the daemon process.
- `relaunch`: Restarts the daemon process.

## Notes
- Ensure the Arduino Nano is connected to the specified port (`/dev/serial/by-id/...`). This can be changed using the PORT constant in the board daemon.
- The daemon uses a Unix socket located at `/tmp/board_daemon.sock`. If the socket file exists but the daemon is not running, it may need to be manually removed.
- The power bar must be connected to the Arduino Nano (pin D2 is hardcoded) and configured to accept logic signals for proper operation.
- The Arduino must be running the standard firmata sketch.