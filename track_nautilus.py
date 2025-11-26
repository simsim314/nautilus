import os
import glob
import subprocess

# 1. Setup Paths
UID = os.getuid()
TRACKER_DIR = f"/run/user/{UID}/nautilus-tracker"

def get_workspace_map():
    """
    Runs 'wmctrl -l' to get a list of open windows.
    Returns a dictionary: { Decimal_ID : Workspace_Number }
    """
    ws_map = {}
    try:
        # wmctrl output looks like: 0x02e00008  0 hostname Title...
        output = subprocess.check_output(["wmctrl", "-l"]).decode("utf-8")
        
        for line in output.splitlines():
            parts = line.split()
            if len(parts) > 2:
                try:
                    # Convert Hex string (0x02e...) to Decimal Integer
                    win_id = int(parts[0], 16)
                    workspace = parts[1]
                    ws_map[win_id] = workspace
                except ValueError:
                    pass
    except FileNotFoundError:
        print("Error: 'wmctrl' is not installed. Run: sudo apt install wmctrl")
        exit(1)
    except Exception as e:
        print(f"Error running wmctrl: {e}")
        exit(1)
        
    return ws_map

def main():
    # Get current window state from OS
    windows = get_workspace_map()
    
    print(f"{'WS':<3} | {'WINDOW ID':<10} | {'PATH'}")
    print("-" * 60)

    # Check tracker directory
    if not os.path.exists(TRACKER_DIR):
        print("No nautilus-tracker directory found.")
        return

    # Look specifically for xid_*.txt files (ignore the old slot_ files)
    files = glob.glob(f"{TRACKER_DIR}/xid_*.txt")
    
    if not files:
        print("No XID tracker files found yet.")
        return

    for filepath in files:
        try:
            with open(filepath, 'r') as f:
                content = f.read().strip()
                # Format is: XID|PATH
                if '|' in content:
                    xid_str, path = content.split('|', 1)
                    xid_int = int(xid_str)
                    
                    # Match with OS data
                    if xid_int in windows:
                        ws_num = windows[xid_int]
                        print(f"{ws_num:<3} | {xid_int:<10} | {path}")
                    else:
                        # Window file exists, but window is not in wmctrl (closed?)
                        print(f"{'?':<3} | {xid_int:<10} | {path} (Not active)")
        except Exception as e:
            print(f"Error reading {filepath}: {e}")

if __name__ == "__main__":
    main()
