from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="skhk_ns2",
    version="1.0.0",
    description=".",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="",
    author="",
    author_email="simmarkalsi1@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["skhk_ns2"],
    include_package_data=True
)
