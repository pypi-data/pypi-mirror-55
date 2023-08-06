from setuptools import setup

with open('README.md') as fd:
    long_description = fd.read()


setup(
    name="igdp-downloader",
    version="1.0.0",
    description="A Python module to download DP of Instagram Profiles in the best quality possible.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="TH3_MA3STRO",
    author_email="satyamjha778@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=["dp_dl"],
    include_package_data=True,
    install_requires=["requests", "bs4"],
    entry_points={
        "console_scripts": [
            "dp-dl=dp_dl.cli:main",
        ]
    }
)