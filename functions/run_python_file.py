import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    working_dir_absolute_path = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_dir_absolute_path, file_path))
    valid_target_path = os.path.commonpath([working_dir_absolute_path, target_file_path]) == working_dir_absolute_path

    if not valid_target_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if os.path.isfile(target_file_path) == False:
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if file_path.endswith(".py") == False:
        return f'Error: "{file_path}" is not a Python file'
    
    try:
        command = ["python", target_file_path]
        if args is not None:
            command.extend(args)

        result_of_the_subprocess = subprocess.run(command, cwd=working_dir_absolute_path, capture_output=True, text=True, timeout=30)
        combined_output = []
        
        
        if result_of_the_subprocess.stdout == "" and result_of_the_subprocess.stderr == "":
            combined_output.append("No output produced")
        if result_of_the_subprocess.stdout != "":
            combined_output.append(f"STDOUT: {result_of_the_subprocess.stdout}")
        if result_of_the_subprocess.stderr != "":
            combined_output.append(f"STDERR: {result_of_the_subprocess.stderr}")
        if result_of_the_subprocess.returncode != 0:
            combined_output.append(f"Process exited with code {result_of_the_subprocess.returncode}")
        return "\n".join(combined_output)

            

    except Exception as e:
        return f"Error: executing Python file: {e}"