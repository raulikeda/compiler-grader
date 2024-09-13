import json
import sys
import os
import shutil


def convert_to_language(content: str, dictionary: str) -> str:

    for key, value in dictionary.items():
        content = content.replace(key, value)

    # return the content
    return content


if __name__ == "__main__":

    # get the first argument
    if len(sys.argv) != 2:
        raise Exception("Invalid arguments. Expected 1 argument: language")
    language = sys.argv[1]

    # open config.json file
    with open("config.json", "r") as f:
        config = json.load(f)

    if language not in config:
        raise Exception("Language not found in config")

    # check if a directory exists for the language
    if os.path.exists(f"./{language}"):
        # delete the directory with all directories and files
        shutil.rmtree(f"./{language}")

    # create a directory for the language
    os.mkdir(f"./{language}")

    # list all directories in Generic directory
    versions = os.listdir("./Generic")

    for version in versions:

        # create a directory for the version
        os.mkdir(f"./{language}/{version}")

        # list all files in the version directory
        files = os.listdir(f"./Generic/{version}")

        for file in files:

            # copy the file to the language/version directory
            with open(f"./Generic/{version}/{file}", "r") as f:
                content = f.read()

            # convert the content to the language if file starts with t
            target = file
            if file[0] == "t":
                content = convert_to_language(content, config[language]["replacements"])
                target = file.replace(
                    ".txt", ".{}".format(config[language]["extension"])
                )

            with open(f"./{language}/{version}/{target}", "w") as f:
                f.write(content)
