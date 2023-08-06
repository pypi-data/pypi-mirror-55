import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="numtmath",
    version="1.6.0.1",
    author="Max Saganyuk",
    author_email="makssagan1@mail.ru",
    description="Module for research in number theory concepts",
    long_description=long_description,
    url="https://github.com/mad-scientist-8/numtmath",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",],
    python_requires=">=3.6"
)
