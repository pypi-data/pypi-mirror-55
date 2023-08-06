from distutils.core import setup
from setuptools import find_packages

setup(
    # Application name:
    name = "IITD_speech_vone",

    # Version number (initial):
    version = "1.0.1",

    # Application author details:
    author= "Anshu Bansal, Jayanth",
    author_email = "cs1160324@iitd.ac.in",

    # Packages
    packages = find_packages(),

    # Include additional files into the package
    include_package_data = True,

    # Details
    url="http://pypi.python.org/pypi/IITD_speech_vone_v101/",

    #
    # license="LICENSE.txt",
    description = "Useful speech recognition and transcription related library for Indian languages.",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
		"pydub",
		"numpy",
		"sklearn",
		"soundfile",
		"pyAudioAnalysis",
		"statistics",
    ],
)
