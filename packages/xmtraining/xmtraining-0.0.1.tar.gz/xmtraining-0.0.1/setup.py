import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xmtraining",
    version="0.0.1",
    author="km",
    author_email="konstantina.mameletzi@xomnia.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[],
    python_requires='>=3.6',
)