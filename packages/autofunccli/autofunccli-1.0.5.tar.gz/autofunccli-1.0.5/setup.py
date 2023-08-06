import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autofunccli", # Replace with your own username,
    packages=setuptools.find_packages(),
    version="1.0.5",
    author="Nicolas Cuadros",
    author_email="cuadros.nicolas@orange.fr",
    description="Transform your function into a command line utility.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CuadrosNicolas/Python-Command-Function",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
