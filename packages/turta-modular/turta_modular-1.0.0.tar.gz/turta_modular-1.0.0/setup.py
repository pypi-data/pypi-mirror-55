import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="turta_modular",
    version="1.0.0",
    author="Turta LLC",
    author_email="hello@turta.io",
    description="Python Libraries for Turta Modular System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.turta.io/modular",
    packages=setuptools.find_packages(),
    install_requires=[
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
        'Documentation': 'https://docs.turta.io',
        'Community': 'https://community.turta.io',
        'GitHub Repository' : 'https://github.com/Turta-io/Modular'
    },
)