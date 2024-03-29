import setuptools

with open("README.md") as f:
    long_description = f.read()

with open("./src/vizplugins/__init__.py") as f:
    for line in f.readlines():
        if line.startswith("__version__"):
            # __version__ = "0.9"
            delim = '"' if '"' in line else "'"
            version = line.split(delim)[1]
            break
    else:
        print("Can't find version! Stop Here!")
        exit(1)

setuptools.setup(
    name="vizplugins",
    version=version,
    author="Tian Gao",
    author_email="gaogaotiantian@hotmail.com",
    description="official plugins for viztracer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gaogaotiantian/vizplugins",
    packages=setuptools.find_packages("src"),
    package_dir={"":"src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        "psutil"
    ],
    python_requires=">=3.7",
)
