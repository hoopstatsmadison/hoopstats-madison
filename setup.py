from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["matplotlib>=3.1.2", "scikit-learn>=0.22.1", "pandas>=0.25.3", "seaborn>=0.10.0"]
setup(
    name="hoopstatsmadison",
    version="0.0.4",
    author="Brandon Jenkins",
    author_email="brandon_jenkins0@icloud.com",
    description="A package for analyzing hoopstats data",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/hoopstatsmadison/hoopstats-madison",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)