import subprocess

def execute_terminal_command(command: str) -> str:
    """
    Execute a specified terminal command and return its output, error message, and exit code.

    This function uses the subprocess module to execute a command in the system's shell. It captures
    the standard output and standard error of the command, along with the exit code. This function
    is useful for automating shell command execution and retrieving its results.

    Args:
        command (str): A valid terminal command to be executed.

    Returns:
        str: the standard output of the command.
    """
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True, check=True)
        print(f"""This command "{command}" is executed and it gives this result :
{result.stdout[:4000]}
""")
        return f"""
For your question, This command "{command}" is executed and it gives this result:
{result.stdout[:4000]}"""
    except subprocess.CalledProcessError as e:
        return f"""
The result of the {command} is :
{e.stderr[:4000]}"""

