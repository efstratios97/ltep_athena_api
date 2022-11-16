import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LTEP Athena API",                     # This is the name of the package
    version="0.0.7",                        # The initial release version
    # Full name of the author
    author="Efstratios Pahis from LTEP Technologies",
    description="The official LTEP Athena API: Welcome to the World's most flexible and extensible Data Science Platform",
    # Long description read from the the readme file
    long_description=long_description,
    long_description_content_type="text/markdown",
    # List of all python modules to be installed
    packages=setuptools.find_packages(include=["ltep_athena_api", "ltep_athena_api.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    license='MIT',
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["ltep_athena_api"],             # Name of the python package
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    # Directory of the source code of the package
    url="https://github.com/efstratios97/ltep_athena_api",
    install_requires=[
    "attrs==22.1.0",
    "autopep8==2.0.0",
    "bidict==0.22.0",
    "certifi==2022.9.24",
    "cffi==1.15.1",
    "charset-normalizer==2.1.1",
    "click==8.1.3",
    "colorama==0.4.6",
    "Deprecated==1.2.13",
    "Flask==2.2.2",
    "Flask-Cors==3.0.10",
    "gevent==22.10.2",
    "greenlet==2.0.1",
    "idna==3.4",
    "iniconfig==1.1.1",
    "itsdangerous==2.1.2",
    "Jinja2==3.1.2",
    "MarkupSafe==2.1.1",
    "multi-key-dict==2.0.3",
    "numpy==1.23.4",
    "packaging==21.3",
    "pandas==1.5.1",
    "pbr==5.11.0",
    "pluggy==1.0.0",
    "pycodestyle==2.9.1",
    "pycparser==2.21",
    "PyGithub==1.57",
    "PyJWT==2.6.0",
    "PyNaCl==1.5.0",
    "pyparsing==3.0.9",
    "python-dateutil==2.8.2",
    "python-engineio==4.3.4",
    "python-jenkins==1.7.0",
    "python-socketio==5.7.2",
    "pytz==2022.6",
    "PyYAML==6.0",
    "Random-Word==1.0.11",
    "randomword==1.0.2",
    "requests==2.28.1",
    "six==1.16.0",
    "tomli==2.0.1",
    "urllib3==1.26.12",
    "websocket-client==1.4.2",
    "Werkzeug==2.2.2",
    "wrapt==1.14.1",
    "zope.event==4.5.0",
    "zope.interface==5.5.1"]
)
