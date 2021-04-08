from setuptools import setup, find_packages
 

def read(file_name):
    return [req.strip() for req in open(file_name).readlines()]


setup(
    name="camara",
    version="0.1.0",
    description="Sistema para câmaras municipais",
    packages=find_packages(exclude=("./venv")),
    include_package_data=True,
    install_requires=read("requirements.txt"),
    extras_require={"dev": read("requirements-dev.txt")},
)
