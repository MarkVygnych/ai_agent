import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    # Will be True or False
    valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    if not valid_target_file:
        return (f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
    if not os.path.isfile(target_file):
        return (f'Error: File not found or is not a regular file: "{file_path}"')
    try:
        with open(target_file, 'r') as f: 
            content = f.read(MAX_CHARS)
            if f.read(1):  # Check if there's more content beyond MAX_CHARS
                return (f'{content} File "{file_path}" truncated at {MAX_CHARS} characters')
            return content
    except Exception as e:
        return (f'Error: Error reading file "{file_path}": {str(e)}')


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads the content of a specified file relative to the working directory",
        "parameters": {
            "type": "object",
            "required": ["file_path"],
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read, relative to the working directory"
                }
            }
        }
    }
}