import argparse
import socket
import subprocess
import os
import time
import signal
from config import SOCKET_ADDRESS, DAEMON_SCRIPT

def ensure_daemon_running():
    if not os.path.exists(SOCKET_ADDRESS):
        print("Daemon is not running. Starting it...")
        subprocess.Popen(["python3", DAEMON_SCRIPT])
        # Wait for the daemon to start
        for i in range(10):
            print(f"Waiting for daemon to start... {i + 1}/10")
            if os.path.exists(SOCKET_ADDRESS):
                print("Daemon started successfully.")
                return
            time.sleep(1)
        print("ERROR: Failed to start the daemon.")
        exit(1)

def kill_daemon():
    if os.path.exists(SOCKET_ADDRESS):
        try:
            # Find the daemon process by its script name
            result = subprocess.run(["pgrep", "-f", DAEMON_SCRIPT], capture_output=True, text=True)
            if result.stdout.strip():
                pid = int(result.stdout.strip())
                os.kill(pid, signal.SIGTERM)
                print(f"Daemon process (PID {pid}) terminated.")
            else:
                print("Daemon process not found, but socket exists. Removing socket.")
        except Exception as e:
            print(f"ERROR: Failed to terminate daemon process: {e}")
        finally:
            os.remove(SOCKET_ADDRESS)
            print("Daemon socket removed.")
    else:
        print("Daemon is not running.")

def relaunch_daemon():
    kill_daemon()
    ensure_daemon_running()

def main():
    parser = argparse.ArgumentParser(description="Control power state.")
    parser.add_argument("action", choices=["on", "off", "status", "kill", "relaunch"], 
                        help="Specify 'on' to power on, 'off' to power off, 'status' to query the current state, 'kill' to stop the daemon, or 'relaunch' to restart the daemon.")
    args = parser.parse_args()

    if args.action == "kill":
        kill_daemon()
        return
    elif args.action == "relaunch":
        relaunch_daemon()
        return

    ensure_daemon_running()

    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.connect(SOCKET_ADDRESS)
            client.sendall(args.action.encode("utf-8"))
            response = client.recv(1024).decode("utf-8").strip()
            print(response)
    except ConnectionRefusedError:
        print("ERROR: Could not connect to the board daemon. Is it running?")

if __name__ == "__main__":
    main()
