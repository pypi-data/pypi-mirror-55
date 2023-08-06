from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="vspyx",
    version="0.0.1",
    description="Vehicle Spy X",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://intrepidcs.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
