import os 
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory) #Get working_directory's absolute path
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory)) #Construct full path to target_dir
        
        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs: #Catching possible errors
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
    
        files_list = os.listdir(target_dir) #List the files in target_dir
        files_data = []
        for filename in files_list: #Iterating over files to build string of data
            filepath = os.path.join(target_dir, filename)
            files_data.append(
                f"- {filename}: file_size={os.path.getsize(filepath)}, is_dir={os.path.isdir(filepath)}"
                )
        return "\n".join(files_data)
    
    except Exception as e:
        return f"Error listing files: {e}"

# Describe function for LLM callers. Tells LLM how functions should be called.
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                    type=types.Type.STRING,
                    description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)