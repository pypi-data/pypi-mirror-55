import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="turta_lorahat",
    version="1.0.0",
    author="Turta LLC",
    author_email="hello@turta.io",
    description="Python Libraries for Turta LoRa HAT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.turta.io/lorahat",
    packages=setuptools.find_packages(),
    install_requires=[
        "pyserial",
        "RPi.GPIO",
        "smbus",
        "spidev"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Topic :: System :: Hardware"
    ],
    project_urls={
        'Documentation': 'https://docs.turta.io/raspberry-pi-hats/lora-hat',
        'Community': 'https://community.turta.io',
        'GitHub Repository' : 'https://github.com/Turta-io/LoRaHAT'
    },
)