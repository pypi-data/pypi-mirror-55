import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bd_metric",
    version="0.0.1",
    author="Shengbin Meng",
    author_email="shengbinmeng@gmail.com",
    description="Bjontegaard metric calculation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shengbinmeng/Bjontegaard_metric",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)