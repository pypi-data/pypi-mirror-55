import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rpi_7segment",
    version="0.0.1",
    author="Anders Gjendem",
    author_email="anders.gjendem@gmail.com",
    description="Library for running 7-segments displays with TPIC6C596 drivers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/agjendem/rpi-7segment",
    packages=setuptools.find_packages(exclude=["tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    setup_requires=['wheel'],
    python_requires='>=3.6',
    test_suite='nose.collector',
    tests_require=['nose'],
)
