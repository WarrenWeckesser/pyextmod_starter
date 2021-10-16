from setuptools import setup


setup(
    name='pyextmod_starter',
    version='0.2.0',
    author='Warren Weckesser',
    description=("Generate boilerplate C code for a Python extension module."),
    license="MIT",
    url="https://github.com/WarrenWeckesser/pyextmod_starter",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="python extension module C",
    py_modules=["pyextmod_starter"],
)
