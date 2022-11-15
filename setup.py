import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LTEP Athena API",                     # This is the name of the package
    version="0.0.6",                        # The initial release version
    # Full name of the author
    author="Efstratios Pahis from LTEP Technologies",
    description="API to connect to LTEP Athena Platform",
    # Long description read from the the readme file
    long_description=long_description,
    long_description_content_type="text/markdown",
    # List of all python modules to be installed
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    license='MIT',
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["ltep_athena_api"],             # Name of the python package
    # Directory of the source code of the package
    url="https://github.com/efstratios97/ltep_athena_api",
    install_requires=["attrs",
                      "autopep8",
                      "bidict",
                      "certifi202",
                      "cffi",
                      "charset-normalizer",
                      "click",
                      "colorama",
                      "Deprecated",
                      "Flask",
                      "Flask-Cors",
                      "Flask-SocketIO",
                      "gevent2",
                      "greenlet",
                      "idn",
                      "iniconfig",
                      "itsdangerous",
                      "Jinja2",
                      "MarkupSafe",
                      "multi-key-dict",
                      "numpy",
                      "packaging",
                      "pandas",
                      "pbr",
                      "pluggy",
                      "pycodestyle",
                      "pycparser",
                      "PyGithub",
                      "PyJWT",
                      "PyNaCl",
                      "pyparsing",
                      "pytest",
                      "python-dateutil",
                      "python-engineio",
                      "python-jenkins",
                      "python-socketio",
                      "pytz",
                      "PyYAM",
                      "Random-Word",
                      "randomword",
                      "requests",
                      "six",
                      "tomli",
                      "urllib31",
                      "websocket-client",
                      "Werkzeug",
                      "wrapt",
                      "zope.event",
                      "zope.interface"]
)
