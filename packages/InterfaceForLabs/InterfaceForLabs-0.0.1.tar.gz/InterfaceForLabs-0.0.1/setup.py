import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="InterfaceForLabs",  # Replace with your own username
    version="0.0.1",
    author="Eugene Budzinskiy",
    author_email="eugene.unusual@gmail.com",
    description="Simple interface for labs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EugeneBudzinskiy/InterfaceForLabs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)