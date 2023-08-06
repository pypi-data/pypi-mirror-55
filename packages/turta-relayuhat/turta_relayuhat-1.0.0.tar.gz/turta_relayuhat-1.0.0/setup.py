import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="turta_relayuhat",
    version="1.0.0",
    author="Turta LLC",
    author_email="hello@turta.io",
    description="Python Libraries for Turta Relay uHAT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.turta.io/relayuhat",
    packages=setuptools.find_packages(),
    install_requires=[
        "RPi.GPIO"
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
        'Documentation': 'https://docs.turta.io/raspberry-pi-hats/relay-uhat',
        'Community': 'https://community.turta.io',
        'GitHub Repository' : 'https://github.com/Turta-io/Relay-uHAT'
    },
)