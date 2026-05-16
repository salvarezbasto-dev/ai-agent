# This is a list of available functions to provide to the LLM

from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ],
)

def call_function(function_call, verbose=False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    #Map function names to actual functions to determine which functions call, if any:
    function_map = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file
    }

    #Checking if name of function_call is in the dict. Return error otherwise.
    function_name = function_call.name or ""

    if function_name not in function_map:
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
            )
        ],
    )

    args = dict(function_call.args) if function_call.args else {} #Make shallow copy of args.
    # We're going to overwrite one argument to ensure the working directory is set properly.

    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./calculator"

    function_result = function_map[function_name](**args)

    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response( #Helper that creates a response for a tool/function call result
            name=function_name,
            response={"result": function_result},
        )
    ],
)

