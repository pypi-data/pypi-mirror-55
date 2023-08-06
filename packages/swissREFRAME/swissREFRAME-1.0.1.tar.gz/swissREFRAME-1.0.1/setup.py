import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='swissREFRAME',
    version='1.0.1',
    author='adal02',
    author_email='hofmann.tobias121@gmail.com',
    description="Python interface for the official swisstopo's REFRAME jar library",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url='https://github.com/adal02/swissREFRAME',
    download_url='https://github.com/adal02/swissREFRAME/archive/V1.0.0.tar.gz',
    install_requires=['JPype1'],
    packages=setuptools.find_packages(),
    include_package_data=True,
    keywords=["geodesy", "geography", "swiss", "coordinates", "transformation"],
    classifiers=[
        'Development Status :: 4 - Beta',
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ]
)
