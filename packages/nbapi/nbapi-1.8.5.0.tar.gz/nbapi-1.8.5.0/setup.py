import setuptools

with open("README.txt", "r") as fh:
    long_description = fh.read()
version="1.8.5.0"
open("version.txt","w+").write(version)
setuptools.setup(
    name="nbapi",
    version=version,
    author="LazyNeko",
    author_email="nekobot.help@gmail.com",
    description="A small anime API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lazyneko1/nbapi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
