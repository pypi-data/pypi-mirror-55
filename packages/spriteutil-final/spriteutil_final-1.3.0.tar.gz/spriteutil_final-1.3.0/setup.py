import setuptools

with open("README.md", "r") as fd:
    long_description = fd.read()

setuptools.setup(
    name="spriteutil_final",
    version="1.3.0",
    author="Long Lam Duc",
    author_email="long.lam@f4.intek.edu.vn",
    description="A sprite detection package",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/intek-training-jsc/sprite-detection-longlamduc.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)