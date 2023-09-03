from setuptools import find_packages, setup

# Read requirements.txt
with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="hpm",
    version="0.1",
    packages=find_packages(),
    install_requires=required,
    # other metadata
    author="JJ Espinoza",
    author_email="jj.espinoza.la@gmail.com",
    description="A project that writes updates",
)
