import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        if os.path.commonpath([working_dir_abs, file_path_abs]) != working_dir_abs: #Catching possible errors
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(file_path_abs, "r", encoding="utf-8") as f: #Opening file
            content = f.read(MAX_CHARS) #Reading file up to MAX_CHARS
            if f.read(1): #Checking if file is larger than the limit
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    
    except Exception as e:
        return f"Error getting file content: {e}"

# Describe function for LLM callers. Tells LLM how functions should be called.
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file in the working directory. Truncated if contents surpass 10000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema( # Check if file_path is correct
                    type=types.Type.STRING,
                    description="File path to open and read file from", 
            ),
        },
        required=["file_path"] # Check
    ),
)