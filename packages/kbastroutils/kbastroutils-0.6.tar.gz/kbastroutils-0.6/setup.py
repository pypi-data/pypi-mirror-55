import setuptools

setuptools.setup(
    name="kbastroutils",
    version="0.6",
    author="Kornpob Bhirombhakdi",
    author_email="kbhirombhakdi@stsci.edu",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bkornpob/example_pkg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6'
)
