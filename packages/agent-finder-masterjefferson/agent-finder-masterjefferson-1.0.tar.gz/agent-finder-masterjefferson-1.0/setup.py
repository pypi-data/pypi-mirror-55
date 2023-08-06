import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="agent-finder-masterjefferson",
    version="1.0",
    author="Jefferson Jones",
    author_email="jeffersonmjones92@gmail.com",
    description="Find nearby auto insurance agents and dump them to a CSV file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/masterjefferson/agent-finder",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'agent-finder = finder.finder:main'
        ]
    },
    install_requires=[
        'googlemaps'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
    ],
    python_requires='>=3.7.5',
)
