import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"], 
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative file path to the target file",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="A string to overwrite the file with",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    working_dir_absolute_path = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(working_dir_absolute_path, file_path))
    valid_target_path = os.path.commonpath([working_dir_absolute_path, target_path]) == working_dir_absolute_path
    
    if valid_target_path == False:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_path) == True:
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    try:
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        open(target_path, "w").write(content,)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
