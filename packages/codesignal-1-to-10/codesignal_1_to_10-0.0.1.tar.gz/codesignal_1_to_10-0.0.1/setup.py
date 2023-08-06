import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="codesignal_1_to_10",
    version="0.0.1",
    author="Kummari Naresh",
    author_email="kummarinaresh35@gmail.com",
    description="Code signals_1_to_10 programs Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/knaresh8464/Codesignals_10_programs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)