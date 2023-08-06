import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TimelineNetworkUtility-zzenlightenzz", # Replace with your own username
    version="0.0.1",
    author="Worawut Boonpeang",
    author_email="",
    description="A small module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="", # https://github.com/pypa/sampleproject
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

# How to
# https://packaging.python.org/tutorials/packaging-projects/
# python --version is 3.*
# python -m pip install --user --upgrade setuptools wheel
# Now run this command from the same directory where setup.py is located:
# python setup.py sdist bdist_wheel
