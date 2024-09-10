# import module compiler-grader using importlib

import importlib

# Import the module
grader = importlib.import_module("compiler-grader.grader")

grader.grade_version("python3 code.py", "v0.1", direct_input=True, maxtime=10, fail_first=False)