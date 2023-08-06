import setuptools
from reminder import version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="status-reminder",
    version=version,
    author="Hongjie Gao",
    author_email="1801213783@pku.edu.cn",
    description="Task status reminder and API exception reminder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alazycoder/Reminder",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)