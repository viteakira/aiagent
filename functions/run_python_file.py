import os
import subprocess


def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_dir]

        if args:
            command.extend(args)

        process = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)

        output_string = ""

        if process.returncode:
            output_string += f"Process exited with code {process.returncode}\n"

        if len(process.stdout) == 0 and len(process.stderr) == 0:
            output_string += "No output produced\n"
        else:
            output_string += f"STDOUT: {process.stdout}\n"
            output_string += f"STDERR: {process.stderr}\n"

        return output_string

    except Exception as e:
        return f"Error: executing Python file: {e}"
