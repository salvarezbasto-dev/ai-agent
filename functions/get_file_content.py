import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        if os.path.commonpath([working_dir_abs, file_path_abs]) != working_dir_abs: #Catching possible errors
            f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path_abs):
            f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(file_path_abs, "r", encoding="utf-8") as f: #Opening file
            content = f.read(MAX_CHARS) #Reading file up to MAX_CHARS
            if f.read(1): #Checking if file is larger than the limit
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    
    except Exception as e:
        return f"Error getting file content: {e}"