import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LTEP Athena API",                     # This is the name of the package
    version="0.0.4",                        # The initial release version
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
    python_requires='>=3.8',                # Minimum version requirement of the package
    py_modules=["ltep_athena_api"],             # Name of the python package
    # Directory of the source code of the package
    url="https://github.com/efstratios97/ltep_athena_api",
    install_requires=['alabaster', 'appdirs', 'APScheduler', 'atomicwrites', 'attrs', 'autopep8', 'Babel', 'bokeh', 'certifi', 'cffi', 'chardet', 'charset-normalizer', 'click', 'click-completion', 'colorama', 'commonmark', 'contextlib2', 'crayons', 'cryptography', 'cycler', 'decorator', 'Deprecated', 'docutils', 'et-xmlfile', 'execnet', 'ez-setup', 'Flask', 'Flask-Cors', 'fonttools', 'future', 'greenlet', 'grpcio', 'grpcio-tools', 'idna', 'imagesize', 'importlib-metadata', 'iniconfig', 'install', 'itsdangerous', 'Jinja2', 'joblib', 'kiwisolver', 'llvmlite', 'MarkupSafe', 'matplotlib', 'mock', 'multi-key-dict', 'nose', 'numpy', 'openpyxl', 'packaging', 'pandas', 'path', 'path.py', 'pbr', 'pip-requirements-parser', 'Pillow', 'pluggy', 'proto-plus', 'protobuf', 'psutil', 'py', 'pycodestyle', 'pycparser', 'PyGithub', 'Pygments', 'PyJWT', 'PyMySQL', 'PyNaCl', 'pyparsing', 'pytest',
                      'pytest-fixture-config', 'pytest-server-fixtures', 'pytest-shutil', 'python-dateutil', 'python-dotenv', 'python-jenkins', 'pytz', 'pytz-deprecation-shim', 'PyYAML', 'Random-Word', 'recommonmark', 'requests', 'retry', 'rinoh-typeface-dejavuserif', 'rinoh-typeface-texgyrecursor', 'rinoh-typeface-texgyreheros', 'rinoh-typeface-texgyrepagella', 'rinohtype', 'scikit-learn', 'scipy', 'seaborn', 'shellingham', 'six', 'sklearn', 'snowballstemmer', 'Sphinx', 'sphinx-rtd-theme', 'sphinxcontrib-applehelp', 'sphinxcontrib-devhelp', 'sphinxcontrib-htmlhelp', 'sphinxcontrib-jsmath', 'sphinxcontrib-qthelp', 'sphinxcontrib-serializinghtml', 'SQLAlchemy', 'SQLAlchemy-Utils', 'termcolor', 'threadpoolctl', 'toml', 'tomli', 'tornado', 'typing_extensions', 'tzdata', 'tzlocal', 'urllib3', 'watchdog', 'Werkzeug', 'wrapt', 'zipp']                     # Install other dependencies if any
)
