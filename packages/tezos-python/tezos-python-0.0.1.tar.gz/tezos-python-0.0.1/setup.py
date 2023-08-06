import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tezos-python",
    version="0.0.1",
    author="Nomadic Labs",
    author_email="",
    description="Python API to run Tezos clients and deamons",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/nomadic-labs/tezos",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'wheel',
        'astroid==2.2.5',
        'atomicwrites==1.3.0',
        'attrs==19.1.0',
        'isort==4.3.17',
        'lazy-object-proxy==1.3.1',
        'mccabe==0.6.1',
        'more-itertools==7.0.0',
        'mypy==0.700',
        'mypy-extensions==0.4.1',
        'pluggy==0.9.0',
        'py==1.8.0',
        'pycodestyle==2.5.0',
        'requests==2.20.1',
        'six==1.12.0',
        'typed-ast==1.3.1',
        'wrapt==1.11.1',
        'base58check==1.0.2',
        'pyblake2==1.1.2',
        'ed25519==1.4',
        'requests==2.20.1',
    ],
    python_requires='>=3.6',
    scripts=['tezos_python/scripts/run_node'],
)
