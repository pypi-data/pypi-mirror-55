import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="bit_cryptocompare",  # Replace with your own username
        version="1.0a1",  # Alpha Release
        author="Aniefiok Friday",
        author_email="frier17@a17s.co.uk",
        description="A Python wrapper for CryptoCompare package",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://gitlab.com/frier17/bit_cryptocompare",
        packages=setuptools.find_packages(),
        keywords="CryptoCompare cryptocurrency",
        classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
                "Intended Audience :: Developers",
        ],
        python_requires='>=3.6',
)
