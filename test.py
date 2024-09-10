# import module compiler-grader using importlib

import importlib

# Import the module
grader = importlib.import_module("compiler-grader.grader")

grader.grade_version("testcode.py", "v0.1")
