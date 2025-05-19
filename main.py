import argparse
import socket
import subprocess
import os
import time
import signal
from config import SOCKET_ADDRESS, DAEMON_SCRIPT, IS_WINDOWS

def is_daemon_running():
    if IS_WINDOWS:
        # Try to connect to TCP port
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(SOCKET_ADDRESS)
            return True
        except (ConnectionRefusedError, OSError):
            return False
    else:
        return os.path.exists(SOCKET_ADDRESS)


def ensure_daemon_running():
    if not is_daemon_running():
        print("Daemon is not running. Starting it...")
        subprocess.Popen(["uv", "run", str(DAEMON_SCRIPT)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Wait for daemon to start
        for i in range(10):
            print(f"Waiting for daemon to start... {i + 1}/10")
            if is_daemon_running():
                print("Daemon started successfully.")
                return
            time.sleep(1)

        print("ERROR: Failed to start the daemon.")
        exit(1)


def kill_daemon():
    print("Attempting to kill daemon...")
    try:
        if IS_WINDOWS:
            # Use taskkill to terminate daemon based on script name
            result = subprocess.run(["tasklist", "/FI", f"IMAGENAME eq uv.exe"], capture_output=True, text=True)
            if DAEMON_SCRIPT.name in result.stdout:
                subprocess.run(["taskkill", "/F", "/IM", "uv.exe"], stdout=subprocess.DEVNULL)
                print("Daemon process terminated.")
            else:
                print("Daemon process not found.")
        else:
            result = subprocess.run(["pgrep", "-f", str(DAEMON_SCRIPT)], capture_output=True, text=True)
            if result.stdout.strip():
                pid = int(result.stdout.strip())
                os.kill(pid, signal.SIGTERM)
                print(f"Daemon process (PID {pid}) terminated.")
            else:
                print("Daemon process not found.")
            # Clean up Unix socket file
            if os.path.exists(SOCKET_ADDRESS):
                os.remove(SOCKET_ADDRESS)
                print("Daemon socket removed.")
    except Exception as e:
        print(f"ERROR: Failed to terminate daemon process: {e}")


def relaunch_daemon():
    kill_daemon()
    ensure_daemon_running()


def send_command(action):
    try:
        if IS_WINDOWS:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect(SOCKET_ADDRESS)
                client.sendall(action.encode("utf-8"))
                response = client.recv(1024).decode("utf-8").strip()
                print(response)
        else:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
                client.connect(SOCKET_ADDRESS)
                client.sendall(action.encode("utf-8"))
                response = client.recv(1024).decode("utf-8").strip()
                print(response)
    except ConnectionRefusedError:
        print("ERROR: Could not connect to the board daemon. Is it running?")


def main():
    parser = argparse.ArgumentParser(description="Control power state.")
    parser.add_argument("action", choices=["on", "off", "status", "kill", "relaunch"],
                        help="Specify 'on' to power on, 'off' to power off, 'status' to query the current state, 'kill' to stop the daemon, or 'relaunch' to restart the daemon.")
    args = parser.parse_args()

    if args.action == "kill":
        kill_daemon()
    elif args.action == "relaunch":
        relaunch_daemon()
    else:
        ensure_daemon_running()
        send_command(args.action)


if __name__ == "__main__":
    main()
