from compiler_grader.grader import grade_version
import sys

if __name__ == "__main__":

    if len(sys.argv) != 3:
        raise Exception("Invalid arguments. Expected 2 arguments: file and version")

    if sys.argv[1][-3:] != ".py":
        raise Exception("Invalid file extension. Expected .py file")

    if sys.argv[2][0] != "v" and sys.argv[2][2] != ".":
        raise Exception("Invalid version pattern. Expected vX.X")

    versions = [
        "v0.1",
        "v1.0",
        "v1.1",
        "v1.2",
        "v2.0",
        "v2.1",
        "v2.2",
        "v2.3",
        "v2.4",
        "v3.0",
        "v3.1",
    ]

    if sys.argv[2] not in versions:
        raise Exception("Invalid version. Expected vX.X")

    grade_version(sys.argv[1], sys.argv[2])
