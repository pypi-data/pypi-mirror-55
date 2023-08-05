"""Python package description."""
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mitemp_cgg1',
    version='0.0.1',
    description='Library to read data from Xiaomi Clear Grass Thermometer Hygrometer sensor with E-Ink',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/KalininAndreyVictorovich/mitemp_cgg1',
    author='Andrey',
    author_email='kalininandreyvictorovich@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: System :: Hardware :: Hardware Drivers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(),
    install_requires=['bluepy==1.3.0'],
    keywords='temperature humidity sensor bluetooth low-energy ble Xiaomi ClearGrass',
)
