from setuptools import setup, find_packages

setup(
    name="compiler_grader",
    version="0.1.0",
    author="Raul Ikeda",
    author_email="rauligs@insper.edu.br",
    description="Lib for autograding the compiler project from the book",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rikeda/compiler-grader",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        # Add dependencies here
    ],
)
