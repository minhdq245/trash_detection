from setuptools import setup, find_packages

setup(
    name="waste-detection",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        line.strip()
        for line in open("requirements.txt").readlines()
        if not line.startswith(("-", "--"))
    ],
    python_requires=">=3.10,<3.11",
)
