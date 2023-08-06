import os
from setuptools import setup
from setuptools.command.install import install
from sys import executable
from ast import literal_eval

# NOTE: setuptools doesn't provide an uninstall script :/
class PostInstallCommand(install):
    def run(self):
        # Run the script to install itself as a systemd unit
        if literal_eval(os.environ.get("SYSTEMD_INSTALL", "False")):
            from subprocess import check_call
            check_call([executable, "dockershield", "--systemd-install"])
        install.run(self)

# Use the requirements.txt
with open("requirements.txt", "r") as f:
    requirements = f.readlines()

# setuptools compatible interface.
setup(
    name="dockershield",
    version="0.0.1",
    author="Sam Moore",
    author_email="smoore@elementengineering.com.au",
    description=(
        "Interface to protect your docker socket, so that you can pass it to containers but prevent them running dangerous commands"
    ),
    license="BSD",
    keywords="docker",
    url="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License"
    ],
    scripts=["scripts/dockershield"],
    packages=["dockershield"],
    install_requires=[
        # Read directly from requirements.txt
        requirements
    ],
    # Include all files in MANIFEST.in
    include_package_data=True,
    # For post installation scripts
    cmdclass={
        "install" : PostInstallCommand
    }
)
