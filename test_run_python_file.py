from functions.run_python_file import run_python_file

def test_run_python_file():
    result = run_python_file("calculator", "main.py") #(should print calculator's instructions)
    print(result)

    result = run_python_file("calculator", "main.py", ["3 + 5"]) #(should run the calculator)
    print(result)

    result = run_python_file("calculator", "tests.py") #(should run tests successfully)
    print(result)

    result = run_python_file("calculator", "../main.py") #(this should return an error)
    print(result)

    result = run_python_file("calculator", "nonexistent.py") #(this should return an error)
    print(result)
    
    result = run_python_file("calculator", "lorem.txt") #(this should return an error
    print(result)

if __name__ == "__main__":
    test_run_python_file()