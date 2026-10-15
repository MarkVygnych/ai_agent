import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    # Will be True or False
    valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    if not valid_target_file:
        return (f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
    if not os.path.isfile(target_file):
        return (f'Error: "{file_path}" does not exist or is not a regular file')
    if not file_path.endswith(".py"):
        return (f'Error: "{file_path}" is not a Python file')

    command = ["python", target_file]
    if args:
        command.extend(args)
   
    try:
        result = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)
        return_message = ""
        if result.returncode != 0:
            return_message += (f'Process exited with code {result.returncode}')
        if result.stdout == "" and result.stderr == "":
            return_message += (f"No output produced")
        else:
            return_message += (f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    except Exception as e:
        return (f"Error: executing Python file: {e}")

    return return_message

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specified Python file relative to the working directory and returns its output",
        "parameters": {
            "type": "object",
            "required": ["file_path"],
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory"
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of arguments to pass to the Python script"
                    },
            }
                }
            }
        }