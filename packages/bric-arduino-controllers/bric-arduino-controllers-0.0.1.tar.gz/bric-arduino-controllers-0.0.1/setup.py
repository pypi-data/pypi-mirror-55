import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bric-arduino-controllers",
    version="0.0.1",
    author="Brian Carlsen",
    author_email="carlsen.bri@gmail.com",
    description="Packages for controlling Arduino devices.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['arduino', 'scpi'],
    url="https://github.com/bicarlsen/bric-arduino-controllers",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha"
    ],
    install_requires=[
        'pyserial'
    ],
    package_data={
        'arduino_json_controller': [ 'json-controller/*' ],
        'arduino_scpi_controller': [ 'scpi_controller/*[!RGBUV_Controller/]*' ]
    }
)