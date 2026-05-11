import os
from config import character_limit
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the contents of a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative file path to the target file",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    working_dir_absolute_path = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(working_dir_absolute_path, file_path))
    valid_target_path = os.path.commonpath([working_dir_absolute_path, target_path]) == working_dir_absolute_path

    if valid_target_path == False:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if os.path.isfile(target_path) == False:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        file_contents = open(target_path)
        file_contents_until_limit = file_contents.read(character_limit)
        if file_contents.read(1):
            file_contents_until_limit += f'[...File "{file_path}" truncated at {character_limit} characters]'
        return file_contents_until_limit

    except Exception as error:
        return f"Error: {error}"
