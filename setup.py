import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="KPUMorgorithm-classification-server", # Replace with your own username
    version="0.0.1",
    author="outstandingboy",
    author_email="outstanding1301@gmail.com",
    description="classification-server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oustanding1301/classification-server",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
