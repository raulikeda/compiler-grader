# Function to grade specific compiler version
# See the book for more details
import subprocess
import os

def grade_version(command: str, version: str, direct_input: bool = True, maxtime: int = 10, fail_first: bool = False) -> str:


    # Get the current file path
    current_file_path = __file__

    # Get the directory of the current file
    current_directory = os.path.dirname(current_file_path)
    
    print(current_directory)

    # List all the files in the tests/version directory
    files = os.listdir(f'{current_directory}/tests/{version}')

    # sort the list to get right test order
    files.sort()

    errors = []

    for file in files:

        # if file starts with letter t
        if file[0] != 't':
                
            # Get the path to the file
            path = f'{current_directory}/tests/{version}/{file}'

            case = int(file[1:4])

            # Read file content
            if direct_input:
                with open(path, 'r') as f:
                    content = f.read()
            else:
                # Get absolute path for the file
                path = os.path.abspath(path)
                # Content will be the file with path as argument
                content = f'{path}/{file}'

            # Read the solution file starting with letter s
            with open(f'{current_directory}/tests/{version}/s{case:03d}.txt', 'r') as f:
                solution = f.read()

            try:
                # Run the command with content as argument and get the output
                output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=content.encode('utf-8'), timeout=maxtime)

            except subprocess.TimeoutExpired:

                report = f"Test {case}: FAIL\n"
                report += f"Input:\n````"
                report += get_test_content(path, direct_input) + "\n"
                report += "````\n\n"
                report += f"Error: Timeout, took too long to execute. Timeout: {maxtime} seconds\n"

                raise Exception(report)

            # Check if the return code is 0 (success)
            if output.returncode == 0:
                # Compare the output with the solution
                if output != solution:
                    
                    report = f"Test {case}: FAIL\n"
                    report += f"Input:\n````"
                    report += get_test_content(path, direct_input) + "\n"
                    report += "````\n\n"
                    report += f"Expected output:\n````\n{solution}\n````\n"
                    report += f"Actual output:\n````\n{output}\n````\n"

                    # If fail_first is True, raise an exception immediately
                    if fail_first:
                        raise Exception(report)

                    # Add the report to the errors list
                    errors.append(report)

            else: # If the return code is not 0 (error)
                # Compare the output with the error tag
                if solution != '[ERROR]':

                    report = f"Test {case}: FAIL\n"
                    report += f"Input:\n````"
                    report += get_test_content(path, direct_input) + "\n"
                    report += "````\n\n"
                    report += f"Expected output:\n````\nError\n````\n"
                    report += f"Actual output:\n````\n{output}\n````\n"

                    # If fail_first is True, raise an exception immediately
                    if fail_first:
                        raise Exception(report)

                    # Add the report to the errors list
                    errors.append(report)


# Get the test content from a file or direct input
def get_test_content(test: str, direct_input: bool = True) -> str:
    if direct_input: # if direct input, test will be the content
        return test
    else: # if not, read the file content
        with open(test, 'r') as f:
            return f.read()

