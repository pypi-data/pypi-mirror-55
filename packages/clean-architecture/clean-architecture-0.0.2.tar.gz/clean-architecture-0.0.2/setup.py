import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="clean-architecture",
    version="0.0.2",
    author="jaystevency",
    author_email="yjy1129@kookmin.ac.kr",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/JayStevency/clean-architecture",
    download_url="https://github.com/JayStevency/clean-architecture",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
