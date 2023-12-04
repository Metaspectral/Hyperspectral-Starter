#!/usr/bin/python
import subprocess
import shutil
import sys
import os


def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""
    return shutil.which(name) is not None


def run_script(shell, script_path, args):
    try:
        subprocess.run([shell, script_path] + args, check=True)
        print(f"Script executed successfully with {shell}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the script: {e}", file=sys.stderr)


# Get the directory of the current Python script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct paths to the Bash and PowerShell scripts
bash_script = os.path.join(script_dir, "run.sh")
powershell_script = os.path.join(script_dir, "run.ps1")

# Get additional command line arguments
additional_args = sys.argv[1:]

bash_available = is_tool("bash")
powershell_available = is_tool("powershell")
pwsh_available = is_tool("pwsh")

if bash_available:
    run_script("bash", bash_script, additional_args)
elif powershell_available:
    run_script("powershell", powershell_script, additional_args)
elif pwsh_available:
    run_script("pwsh", powershell_script, additional_args)
else:
    print("Neither Bash nor PowerShell is available.", file=sys.stderr)
