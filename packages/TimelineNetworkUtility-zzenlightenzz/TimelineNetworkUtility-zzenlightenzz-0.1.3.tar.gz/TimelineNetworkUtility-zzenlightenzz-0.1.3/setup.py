import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TimelineNetworkUtility-zzenlightenzz", # Replace with your own username
    version="0.1.3",
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
    python_requires='>=3.6', # 3.6
)

# How to
# https://medium.com/@thucnc/how-to-publish-your-own-python-package-to-pypi-4318868210f9
# https://packaging.python.org/tutorials/packaging-projects/
# python --version is 3.*
# python -m pip install --user --upgrade setuptools wheel
# Now run this command from the same directory where setup.py is located:
# python setup.py sdist bdist_wheel
# Uploading the distribution archives
# python -m pip install --user --upgrade twine
# Upload
# python -m twine upload dist/*
# https://pypi.org/project/TimelineNetworkUtility-zzenlightenzz/0.0.1/
# If Reupload dont forget remove old file in dist folder and change version of reupload file
# python setup.py sdist bdist_wheel
# python -m twine upload dist/*
# https://docs.python.org/3/distutils/sourcedist.html#specifying-the-files-to-distribute
# specify additional files to distribute
# https://stackoverflow.com/questions/38394362/distribute-pip-package-no-source-code
