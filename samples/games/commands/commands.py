import subprocess

def run_command_on_server(command: str):
    subprocess.run(["/home/steve/scripts/mc-command.sh", command])

def run_command_script_on_server(name: str):
    f = open(f"/home/steve/samples/games/commands/{name}.txt", "r")
    for line in f.readlines():
        run_command_on_server(line)

def run_standard_setup():
    run_command_script_on_server("standard")