#!/usr/bin/env python

######################################################
##          TBM - Tunnel Boring Machine
######################################################
## A Manager for SSH Tunnels
# Open, save, close, and monitor tunnels

import pathlib
import argparse
import json
import subprocess
import psutil
import fnmatch
import signal

######################################################
##          GLOBALS
######################################################

# Config file path and name relative to ~/
config_file = ".config/tbm/config.json"

# Keys that every 'tunnel' type must have to be complete
tunnel_required_keys = ["name", "remote_username", "remote_server", "local_port",  "remote_hostname", "remote_port", "ssh_port"]


######################################################
##          CLASSES
######################################################

# Class of ANSI color codes
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Class of a tunnel object
class tunnel:
    def __init__(self, name=None, remote_username=None, remote_server=None, local_port=None, remote_hostname=None, remote_port=None, ssh_port=None):
        self.name = name
        self.remote_username = remote_username
        self.remote_server = remote_server
        self.local_port = local_port
        self.remote_hostname = remote_hostname
        self.remote_port = remote_port
        self.ssh_port = ssh_port

    def __eq__(self, other):
        if not isinstance(other, tunnel):
            return NotImplemented
        # else (implied)

        return (self.remote_username == other.remote_username and
                self.remote_server == other.remote_server and
                self.local_port == other.local_port and
                self.remote_hostname == other.remote_hostname and
                self.remote_port == other.remote_port and
                self.ssh_port == other.ssh_port)

######################################################
##          FUNCTIONS
######################################################

# Set up argument parsing and do it
def get_user_args():
    # Set up the argument handling function
    parser = argparse.ArgumentParser(description="Manager of SSH tunnels, see open tunnels, open new ones, and close old ones.")

    # Add arguments
    parser.add_argument("command", nargs="?", default="list", help="open, close, list")
    parser.add_argument("name", nargs="?", default=None, help="tunnel name or \"saved\" to list tunnel names in config")
    
    # Do the actual parsing
    args = parser.parse_args()
    return args


# Creates tunnel object from a dict and global settings
# returns None for tunnel that has an error
def fill_from_global(tunnel_name, tunnel_dict, globals_dict):
    # Return tunnel object
    tunnel_obj = tunnel()

    # Set the name since that's given
    tunnel_obj.name = tunnel_name

    # Set all Global settings
    for key in tunnel_required_keys:
        if key in globals_dict:
            setattr(tunnel_obj, key, globals_dict[key])

    # Set all tunnel specific settings
    for key in tunnel_required_keys:
        if key in tunnel_dict:
            setattr(tunnel_obj, key, tunnel_dict[key])

    # Check for attrs that are still None (this indicates an error)
    for key in tunnel_required_keys:
        if getattr(tunnel_obj, key, None) is None:
            # Required key is missing. Print an error and ignore this tunnel
            print("{0}Error, key \"{1}\" not set for tunnel \"{2}\" or in global settings. Tunnel ignored{3}.".format(bcolors.FAIL, key, tunnel_name, bcolors.ENDC))
            return None

    return tunnel_obj


# Load users config Fails if it doesn't exist
def load_config(config_file):
    # User home and config file path
    home = pathlib.Path.home()
    config_path = home / pathlib.PurePath(config_file)

    # Attempt to open the config file and error out if doesn't exist
    try:
        config_file = open(config_path)
    except:
        print("{0}Config file at {1} could not be opened, and is required for the specified operation{2}\n".format(bcolors.FAIL, config_path, bcolors.ENDC))
        quit()

    # Attempt to parse the config file and error out if JSON is bad
    try:
        full_config = json.load(config_file)
    except:
        print("{0}Config file at {1} could not be parsed, and is required for the specified operation{2}\n".format(bcolors.FAIL, config_path, bcolors.ENDC))
        quit()

    # JSON was good
    # Temp vars to make it easier to read down below, partition the config into two big chunks
    tunnels_dict = full_config['tunnels']
    globals_dict = full_config['global']

    # Fill all missing tunnel values from the global config
    return_tunnel_set = []

    for tun_name in tunnels_dict:
        # Temp var to hold the tunnel once its been filled from global settings
        globalized_tunnel = fill_from_global(tun_name, tunnels_dict[tun_name], globals_dict)

        # If return is None, the tunnel is missing a setting that's also not in the globals. It is ignored.
        if globalized_tunnel is not None:
            return_tunnel_set.append(globalized_tunnel)

    return return_tunnel_set


# Print all the tunnels in a list of tunnel objects in a nice table
def print_tunnel_list(tunnels):
    # This stores the column width for each key
    column_width = dict()

    # Find the longest string for each attribute column (including the key name itself)
    for key in tunnel_required_keys:
        column_width[key] = max([max(len(str(getattr(tunnel, key))), len(key)) for tunnel in tunnels])

    # Print the header row in color
    print("{0}".format(bcolors.HEADER))
    for key in tunnel_required_keys:
        print("{0: <{1}}".format(key, column_width[key] + 2), end="|")
    print("")
    
    # Print a line of '=' below the headers and stop color print
    for i in range(sum(column_width[key] + 3 for key in tunnel_required_keys)):
        print("=", end="")
    print("{0}".format(bcolors.ENDC))

    # Print each tunnel as a line
    for tunnel in tunnels:
        # Print the attribute values for the tunnel
        for key in tunnel_required_keys:
            print("{0: <{1}}".format(getattr(tunnel, key), column_width[key]+2), end="|")
        print("")

    return

# List tunnels the user has saved in their config
def list_saved_tunnels(tunnels):
    print_tunnel_list(tunnels)
    return


# Find flag in list and return value
def find_flag(flag, list, rmflag):
    try:
        result = list[list.index(flag) + 1]
    except:
        try:
            result = fnmatch.filter(list, "*" + flag + "*")[0]
        except:
            result = None

        if rmflag == True:
            result = result.split(flag)[1]

    return result

# Turn a list of ssh args into a tunnel dict entry
def parse_ssh_cmd(ssh_cmd):
    tun = tunnel()

    # Get the required args for a local tunnel
    try:
        # Parse the port:host:port arg
        tun.local_port, tun.remote_hostname, tun.remote_port = find_flag("-L", ssh_cmd, True).split(":")
        tun.local_port = int(tun.local_port)
        tun.remote_port = int(tun.remote_port)
        # Parse the user@server arg
        tun.remote_username, tun.remote_server = find_flag("@", ssh_cmd, False).split("@")
    except:
        return None

    # Check for the -p SSH port arg
    try:
        port = find_flag("-p", ssh_cmd, True)
    except:
        tun.ssh_port = 22
    else:
        tun.ssh_port = int(port)

    return tun


# Get open tunnels
def get_open_tunnels(saved_tunnels):
    # List of the ssh connections open
    open_tunnels = []

    # Find all open ssh commands
    for proc in psutil.process_iter():
        if proc.name() == "ssh":
            # Parse SSH command into an object for printing
            tunnel = parse_ssh_cmd(proc.cmdline())

            # Append the tunnel if its a real one
            if tunnel != None:
                # Store the PID
                tunnel.pid = proc.pid

                # Check if its a saved one and add the name if so
                try:
                    tunnel.name = saved_tunnels[saved_tunnels.index(tunnel)].name
                except:
                    tunnel.name = "tun" + str(len(open_tunnels) + 1)

                # Append tunnel to open list
                open_tunnels.append(tunnel)
    
    return open_tunnels

# List tunnels that are currently open
def list_open_tunnels(saved_tunnels):
    # Get open tunnels
    open_tunnels = get_open_tunnels(saved_tunnels)

    # Print open tunnels
    if open_tunnels:
        print_tunnel_list(open_tunnels)
    else:
        print("{0}No open tunnels{1}".format(bcolors.OKBLUE, bcolors.ENDC))

    return


# Open a new tunnel from saved value in config
def open_tunnel(tunnel_name, saved_tunnels):
    # Tunnel we're going to SSH
    tun_to_open = None

    # Find the tunnel specified
    for tunnel in saved_tunnels:
        if tunnel.name == tunnel_name:
            tun_to_open = tunnel
            break

    # Open tunnel if its valid
    if tun_to_open is not None:
        # Create a new SSH Tunnel
        # ssh -L local_port:remote_hostname:remote_port remote_username@remote_server:ssh_port -f -N
        ssh_open_cmd = ["ssh", "-L",
                        "{0}:{1}:{2}".format(tun_to_open.local_port, tun_to_open.remote_hostname, tun_to_open.remote_port),
                        "{0}@{1}".format(tun_to_open.remote_username, tun_to_open.remote_server),
                        "-p{0}".format(tun_to_open.ssh_port),
                        "-f", "-N"]
        subprocess.run(ssh_open_cmd)
    else:
        print("{0}Tunnel \"{1}\" is not in saved list. Check list with \"tbm list saved\"{2}".format(bcolors.FAIL, tunnel_name, bcolors.ENDC))

    return


# Close a currently open tunnel
def close_tunnel(tunnel_name, saved_tunnels):
    # Tunnel to close
    tun_to_close = None

    # Get open tunnels
    open_tunnels = get_open_tunnels(saved_tunnels)

    # Check if tunnel_name is a valid open tunnel
    for tunnel in open_tunnels:
        if tunnel.name == tunnel_name:
            tun_to_close = tunnel
            break

    # Close tunnel if its valid
    if tun_to_close is not None:
        # Close it
        process = psutil.Process(tun_to_close.pid)
        process.send_signal(signal.SIGTERM)

    else:
        # Not found, error
        print("{0}Tunnel \"{1}\" not found in open list{2}".format(bcolors.FAIL, tunnel_name, bcolors.ENDC))
        if open_tunnels:
            print_tunnel_list(open_tunnels)

    return


######################################################
##          MAIN
######################################################
def main():
    # Parse user command line options
    args = get_user_args()

    # Get user config file of tunnels
    saved_tunnels = load_config(config_file)

    ## Perform actions based on args

    # List saved tunnels
    if args.command == "list" and args.name == "saved":
        list_saved_tunnels(saved_tunnels)    
    
    # List open tunnels
    elif args.command == "list" and args.name == None:
        list_open_tunnels(saved_tunnels)

    # Open a new tunnel
    elif args.command == "open" and args.name != None:
        open_tunnel(args.name, saved_tunnels)

    # Close an active tunnel
    elif args.command == "close" and args.name != None:
        close_tunnel(args.name, saved_tunnels)

    # Illegal set of args
    else:
        print("{0}Arguments provided are not right{1}".format(bcolors.FAIL, bcolors.ENDC))



## Actually call main
main()