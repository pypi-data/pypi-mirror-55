import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-thanos", # Replace with your own username
    version="0.0.1",
    author="Prabhu Pant",
    author_email="prabhupant09@gmail.com",
    description="Uninstall your current virtual environment packages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prabhupant/py-thanos",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
