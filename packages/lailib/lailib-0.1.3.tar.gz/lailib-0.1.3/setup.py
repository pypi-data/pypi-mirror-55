import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lailib", # Replace with your own username
    version="0.1.3",
    author="learnable.ai",
    author_email="contact@learnable.ai",
    description="A bag of helper functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/learnable-ai/lailib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
