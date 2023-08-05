from setuptools import setup, find_packages

def yield_requirements(filename):
    " Yield requirements from a pip requirements.txt file "
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                yield line

def readfile(filename):
    " Opend and read a file "
    with open(filename, "r") as f:
        return f.read()

if __name__ == "__main__":

    setup(
        name="videoframes",
        version="0.0.1",
        author="Jeffrey Spiers",
        author_email="jeffrey.spiers@mail.mcgill.ca",
        description="Extract/assemble frame images from/to a video file",
        long_description=readfile("README.md"),
        long_description_content_type="text/markdown",
        url="https://gitlab.com/jspiers/videoframes",
        packages=find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        scripts=["scripts/videoframes"],
        install_requires=list(yield_requirements("requirements.txt")),
        python_requires='>=3.5',
    )
