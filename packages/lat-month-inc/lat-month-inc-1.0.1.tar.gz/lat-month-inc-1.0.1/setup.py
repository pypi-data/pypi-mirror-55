from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="lat-month-inc",
    version="1.0.1",
    description="A Python package that input pandas dataframe and gives you the next calendar month date column embedded.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/arundubey6215/lat-month-inc",
    author="Samar Dubey",
    author_email="adudubey2615@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["latitude_mon_inc"],
    include_package_data=True,
)