import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="UH_pyOPCN3",
    version="0.0.1",
    author="Joseph Girdwood",
    author_email="j.girdwood@herts.ac.uk",
    description="Library for interfacing and logging data from the Alphasense OPC-N3 developed at the university of "
                "Hertfordshire. Please submit bug reports to https://github.com/JGirdwood/UH_pyOPCN3/projects/1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JGirdwood/UH_pyOPCN3",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    install_requires=[
        'spidev',
        'gpiozero',
        'struct',
    ],
)
