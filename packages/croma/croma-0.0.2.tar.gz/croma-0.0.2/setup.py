import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="croma",
    version="0.0.2",
    author="Fidel Echevarria Corrales",
    author_email="fidel.echevarria.corrales@gmail.com",
    description="A simple scientific visualization and animation library for Python",
    url="https://github.com/fidelechevarria/croma",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)