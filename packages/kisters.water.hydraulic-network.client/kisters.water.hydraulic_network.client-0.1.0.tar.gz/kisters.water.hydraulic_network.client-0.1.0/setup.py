from os import path

from setuptools import find_namespace_packages, setup


# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="kisters.water.hydraulic_network.client",
    use_scm_version=True,
    author="Jesse VanderWees",
    author_email="jesse.vanderwees@kisters-bv.nl",
    description="Client library for the Kisters Hydraulic Network Storage service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/kisters/water/hydraulic-network/client",
    packages=find_namespace_packages(include=["kisters.*"]),
    zip_safe=False,
    install_requires=[
        "kisters.water.hydraulic_network.models",
        "kisters.water.rest_client",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Operating System :: OS Independent",
    ],
)
