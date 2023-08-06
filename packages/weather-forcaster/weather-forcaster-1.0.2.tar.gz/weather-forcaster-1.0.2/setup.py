from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="weather-forcaster",
    version="1.0.2",
    description="A Python package to get weather forcast for any location.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/ragubass/weather-forcaster",
    author="Ragu Sekaran",
    author_email="seleniumragu@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["weather_forcaster"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "weather-forcaster=weather_forcaster.main:main",
        ]
    },
)