import os 

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory) #Get working_directory's absolute path
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory)) #Construct full path to target_dir
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs #Boolean. Check if target_dir falls within working_directory's absolute path
        
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