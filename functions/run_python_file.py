import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory) #Get working_directory's absolute path
        file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if os.path.commonpath([working_dir_abs, file_path_abs]) != working_dir_abs: #Catching possible errors
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path_abs.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        #Creating subprocess to run the file
        command = ["python", file_path_abs] 
        if args:
            command.extend(args) #Add args to list if they were provided
        
        completed_process = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            timeout=30,
            text=True
            ) #Run the subprocess and store the output in a variable.
        #In the signature, we set the current working directory to working_dir_abs,
        #capture stdout and stderr, set a timeout of 30 secs,
        #and decode output to strings instead of bytes.

        output_str = [] #Building output string based on completed_process 
        if completed_process.returncode != 0:
            output_str.append(f"Process exited with code {completed_process.returncode}")
        if not completed_process.stdout.strip() and not completed_process.stderr.strip(): #Using strip() to check for 'no output.'
            output_str.append("No output produced")
        if completed_process.stdout: #Checking for text produced by stdout or stderr
            output_str.append(f"STDOUT: {completed_process.stdout}")
        if completed_process.stderr:
            output_str.append(f"STDERR: {completed_process.stderr}")
        
        return '\n'.join(output_str) #Returning full output string
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
