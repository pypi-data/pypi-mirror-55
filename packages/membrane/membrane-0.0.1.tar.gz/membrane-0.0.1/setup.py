import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="membrane",  # Replace with your own username
    version="0.0.1",
    author="jscul",
    author_email="cullen.scott.john@gmail.com",
    description="A Flask and Flask-RESTful argument parser.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jscul/membrane.py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
