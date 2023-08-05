import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

with open("LICENSE", "r") as f:
    license = f.read()

setuptools.setup(
    name="aeromiko",
    version="0.0.1",
    author="Andy Truett",
    author_email="andrew.truett@gmail.com",
    description="A small example package",
    long_description=long_description,
    license=license,
    keywords="aerohive netmiko",
    url="https://github.com/andytruett/aeromiko",
    packages=setuptools.find_packages(),
    install_requires=["netmiko>=2.4.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
