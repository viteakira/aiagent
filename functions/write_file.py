import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_dir), mode=0o777, exist_ok=True)

        with open(target_dir, "w") as f:
            f.write(content)

            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes the given content to a file relative to the working directory, creates it if it does not exist, otherwise overwrites it",
        "parameters": {
            "required": [
                "file_path",
                "content",
            ],
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to write to the file, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "The content that will be written to the file",
                },
            },
        },
    },
}
