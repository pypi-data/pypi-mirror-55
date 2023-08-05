import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="point_pypi_demo",
    version="0.0.1",
    author="Point",
    description="point world",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pointworld/point_pypi_demo",
    packages=setuptools.find_packages(),
    install_requires=['numpy==1.14.4'],
    entry_points={
        'console_scripts': [
            'point_pypi_demo=point_pypi_demo:main'
        ]
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    )
)
