import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pylastic-peshane",
    version="0.0.2",
    author="Laurent Fuentes",
    author_email="social@peshane.net",
    description="Interact with Jelastic API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/laurentfufu/pylastic",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)
