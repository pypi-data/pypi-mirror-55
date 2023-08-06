import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pydiscotool-cli',
    version='0.1.3',
    author="Daniel Carrera",
    author_email="daniel.r.carrera@outlook.com",
    description="A cli for a suite of python tools to help with Disco",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Wundr-Disco/pydiscotool-cli",

    packages=["pydiscotool-cli"],

    install_requires=[
        'click',
        'pydiscotools'
    ],

    entry_points='''
        [console_scripts]
        pydiscotool=pydiscotool.init:main
    ''',

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
