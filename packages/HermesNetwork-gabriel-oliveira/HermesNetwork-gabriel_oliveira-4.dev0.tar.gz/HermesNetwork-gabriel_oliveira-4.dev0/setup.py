import setuptools

with open("README.txt", "r") as fh:
        long_description = fh.read()

setuptools.setup(
    name="HermesNetwork-gabriel_oliveira", # Replace with your own username
    version="04.dev",
    author="Gabriel De Oliveira",
    author_email="gabriel.oli01001@gmail.com",
    description="A high speed networks system",
    long_description=long_description,
    long_description_content_type="text/plain",
    url="https://test.pypi.org/legacy/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    python_requires='>=3.6',
    )
