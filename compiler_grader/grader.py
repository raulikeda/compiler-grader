# Function to grade specific compiler version
# See the book for more details
import subprocess
import os
import sys
import json


def grade_version(file: str, version: str, language: str = "C", **kwargs) -> str:

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

    # Get the current file path
    current_file_path = __file__

    # Get the directory of the current file
    current_directory = os.path.dirname(current_file_path)

    # Check if tests directory exists
    if not os.path.exists(f"{current_directory}/tests/{language}"):
        raise Exception(f"Tests for {language} not found")

    # get extension from config.json
    extension = json.load(open(f"{current_directory}/tests/config.json"))[language][
        "extension"
    ]

    direct_input = True
    if int(version[1]) >= 2:
        direct_input = False

    errors = run_test_files(
        language,
        f"{interpreter} {file}",
        version,
        extension,
        direct_input=direct_input,
        **kwargs,
    )

    for error in errors:
        print("-" * 50)
        print(error.replace("````", ""))


def run_test_files(
    language: str,
    command: str,
    version: str,
    extension: str,
    direct_input: bool = True,
    maxtime: int = 10,
    fail_first: bool = False,
) -> list:

    # Get the current file path
    current_file_path = __file__

    # Get the directory of the current file
    current_directory = os.path.dirname(current_file_path)

    # Open json meta file from test and version
    meta = json.load(open(f"{current_directory}/tests/{language}/{version}/meta.json"))

    errors = []

    for i in range(1, len(meta) + 1):
        file = f"{current_directory}/tests/{language}/{version}/t{i:03d}.{extension}"

        # Read file content
        if direct_input:
            with open(file, "r") as f:
                content = f.read()
        else:
            content = file

        # Read the solution file starting with letter s
        with open(
            f"{current_directory}/tests/{language}/{version}/s{i:03d}.txt", "r"
        ) as f:
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

            report = f"Test {i}: FAIL\n"
            report += f"Input:\n````"
            report += get_test_content(content, direct_input)
            report += "````\n\n"
            report += f"Error: Timeout, took too long to execute. Timeout: {maxtime} seconds\n"

            raise Exception(report)

        # Check if the return code is 0 (success)
        if output.returncode == 0:

            # Compare the output with the solution
            if output.stdout.decode("utf-8").strip() != solution.strip():

                report = f"Test {i}: FAIL\n"
                report += f"Description: {meta[i-1]['Description']}\n"
                report += f"Input:\n````"
                report += get_test_content(content, direct_input)
                report += "````\n\n"
                if solution == "[ERROR]":
                    report += f"Expected output:\n````{meta[i-1]['Result']}\n````\n"
                else:
                    report += f"Expected output:\n````{solution}````\n"
                report += f"Actual output:\n````{result}````\n"

                # If fail_first is True, raise an exception immediately
                if fail_first:
                    raise Exception(report)

                # Add the report to the errors list
                errors.append(report)

        else:  # If the return code is not 0 (error)
            # Compare the output with the error tag
            if solution != "[ERROR]":

                report = f"Test {i}: FAIL\n"
                report += f"Description: {meta[i-1]['Description']}\n"
                report += f"Input:\n````"
                report += get_test_content(content, direct_input)
                report += "````\n\n"
                report += f"Expected output:\n````{meta[i-1]['Result']}\n````\n"
                report += f"Actual output:\n````Error````\n"

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
