import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if os.path.commonpath([working_dir_abs, file_path_abs]) != working_dir_abs: #Catching possible errors
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(file_path_abs):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        parent_dir = os.path.dirname(file_path_abs)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True) #Checking that parent directories of file_path exist

        with open(file_path_abs, "w") as f: #Open file in write mode
            f.write(content) #Overwrite its contents with 'content'
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error writing files: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file in the working directory, creating parent directories if needed.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write into the target file",
            ),
        },
        required=["file_path", "content"],
    ),
)