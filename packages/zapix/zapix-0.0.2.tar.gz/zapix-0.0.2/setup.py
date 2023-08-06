import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zapix", # Replace with your own username
    version="0.0.2",
    author="Nikolay Lebedev",
    author_email="fifo.mail@gmail.com",
    description="Zabbix api wrapper",
    long_description="Zabbix api wrapper",
    long_description_content_type="text/markdown",
    url="https://github.com/bakaut/zapix",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.6',
)