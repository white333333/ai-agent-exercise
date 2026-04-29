import os

def get_files_info(working_directory, directory="."):
    working_dir_absolute_path = os.path.abspath(working_directory)
    target_directory = os.path.normpath(os.path.join(working_dir_absolute_path, directory))
    valid_target_dir = os.path.commonpath([working_dir_absolute_path, target_directory]) == working_dir_absolute_path
    
    if valid_target_dir == False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if os.path.isdir(target_directory) == False:
        return f'Error: "{directory}" is not a directory'
    
    try:
        combined_lines_of_content = []
        for item in os.listdir(target_directory):
            combined_lines_of_content.append(f"- {item}: file_size={os.path.getsize(os.path.join(target_directory, item))} bytes, is_dir={os.path.isdir(os.path.join(target_directory, item))}")
        return "\n".join(combined_lines_of_content)
    except Exception as e:
        return f"Error: {e}"
