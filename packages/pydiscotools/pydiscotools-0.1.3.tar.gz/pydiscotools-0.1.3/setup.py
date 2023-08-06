import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pydiscotools',
    version='0.1.3',
    author="Daniel Carrera",
    author_email="daniel.r.carrera@outlook.com",
    description="A suite of python tools to help with Disco",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Wundr-Disco/pydiscotools",

    packages=setuptools.find_packages(),

    install_requires=[
        'tensorflow',
        'pandas'
    ],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
