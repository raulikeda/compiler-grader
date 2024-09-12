# Function to grade specific compiler version
# See the book for more details
import subprocess
import os
import sys


def grade_version(file: str, version: str, **kwargs) -> str:

    # Get the intepreter
    interpreter = sys.executable

    # check if version patten is correct vn.n
    if not version[0] == "v" and version[2] == ".":
        raise Exception("Invalid version pattern")

    # Check if the file exists
    if not os.path.exists(file):
        raise Exception("File not found")

    # Check if the file is a python file
    if not file.endswith(".py"):
        raise Exception("File is not a python file")

    direct_input = True
    if int(version[1]) >= 2:
        direct_input = False

    errors = run_test_files(
        f"{interpreter} {file}", version, direct_input=direct_input, **kwargs
    )

    for error in errors:
        print(error.replace("````", ""))


def run_test_files(
    command: str,
    version: str,
    direct_input: bool = True,
    maxtime: int = 10,
    fail_first: bool = False,
) -> str:

    # Get the current file path
    current_file_path = __file__

    # Get the directory of the current file
    current_directory = os.path.dirname(current_file_path)

    # List all the files in the tests/version directory
    files = os.listdir(f"{current_directory}/tests/{version}")

    # sort the list to get right test order
    files.sort()

    errors = []

    for file in files:

        # if file starts with letter t
        if file[0] == "t":

            # Get the path to the file
            path = f"{current_directory}/tests/{version}/{file}"

            case = int(file[1:4])

            # Read file content
            if direct_input:
                with open(path, "r") as f:
                    content = f.read()
            else:
                content = path

            # Read the solution file starting with letter s
            with open(f"{current_directory}/tests/{version}/s{case:03d}.txt", "r") as f:
                solution = f.read()

            try:
                # Run the command with content as argument and get the output
                args = command.split(" ")
                args.append(content)
                output = subprocess.run(
                    args,
                    # shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=maxtime,
                )

                result = output.stdout.decode("utf-8").strip()

            # If the process takes too long to execute
            except subprocess.TimeoutExpired:

                report = f"Test {case}: FAIL\n"
                report += f"Input:\n````"
                report += get_test_content(content, direct_input) + "\n"
                report += "````\n\n"
                report += f"Error: Timeout, took too long to execute. Timeout: {maxtime} seconds\n"

                raise Exception(report)

            # Check if the return code is 0 (success)
            if output.returncode == 0:

                # Compare the output with the solution
                if output.stdout.decode("utf-8").strip() != solution.strip():

                    report = f"Test {case}: FAIL\n"
                    report += f"Input:\n````"
                    report += get_test_content(content, direct_input) + "\n"
                    report += "````\n\n"
                    report += f"Expected output:\n````\n{solution}\n````\n"
                    report += f"Actual output:\n````\n{result}\n````\n"

                    # If fail_first is True, raise an exception immediately
                    if fail_first:
                        raise Exception(report)

                    # Add the report to the errors list
                    errors.append(report)

            else:  # If the return code is not 0 (error)
                # Compare the output with the error tag
                if solution != "[ERROR]":

                    print(solution)

                    report = f"Test {case}: FAIL\n"
                    report += f"Input:\n````"
                    report += get_test_content(content, direct_input) + "\n"
                    report += "````\n\n"
                    report += f"Expected output:\n````\{solution}\n````\n"
                    report += f"Actual output:\n````\nError\n````\n"

                    # If fail_first is True, raise an exception immediately
                    if fail_first:
                        raise Exception(report)

                    # Add the report to the errors list
                    errors.append(report)

    return errors


# Get the test content from a file or direct input
def get_test_content(test: str, direct_input: bool = True) -> str:
    if direct_input:  # if direct input, test will be the content
        return test
    else:  # if not, read the file content
        with open(test, "r") as f:
            return f.read()
