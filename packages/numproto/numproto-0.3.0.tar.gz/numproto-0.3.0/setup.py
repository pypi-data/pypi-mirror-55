import glob
import sys

from setuptools import find_packages, setup
from setuptools.command.develop import develop

if sys.version_info < (3, 6):
    sys.exit("Please use Python version 3.6 or higher.")


# get the version
version = {}
with open("numproto/__version__.py") as fp:
    exec(fp.read(), version)

# get readme
with open("README.md", "r") as fh:
    readme = fh.read()


# Handle protobuf
class CustomDevelopCommand(develop):
    def run(self):
        # we need to import this here or else grpc_tools would have to be
        # installed in the system before we could run the setup.py
        from grpc_tools import protoc

        develop.run(self)

        proto_files = glob.glob("./numproto/protobuf/*.proto")
        command = [
            "grpc_tools.protoc",
            "--proto_path=./numproto/protobuf/",
            "--python_out=./numproto/protobuf/",
            "--grpc_python_out=./numproto/protobuf/",
            "--mypy_out=./numproto/protobuf",
        ] + proto_files

        print("Building proto_files {}".format(proto_files))
        if protoc.main(command) != 0:
            raise Exception("error: {} failed".format(command))


install_requires = [
    "numpy~=1.15",  # BSD
    "protobuf~=3.9",  # BSD
    "grpcio~=1.23",  # Apache License 2.0
]

dev_require = [
    "grpcio-tools~=1.23",  # Apache License 2.0
    "isort==4.3.20",  # MIT
    "black==19.3b0",  # MIT
    "mypy==0.720",  # MIT License
    "mypy-protobuf==1.15",  # Apache License 2.0
    "pylint==2.3.1",  # GPL
]

tests_require = ["pytest==5.1.2"]  # MIT


setup(
    name="numproto",
    version=version["__version__"],
    description="NumProto provides NumPy ndarray to protobuf conversion.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/xainag/numproto",
    author="NumProto Contributors",
    author_email="services@xain.io",
    license="Apache License Version 2.0",
    zip_safe=False,
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
    ],
    packages=find_packages(exclude=["tests"]),
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={"test": tests_require, "dev": dev_require + tests_require},
    cmdclass={"develop": CustomDevelopCommand},
    package_data={"numproto": ["protobuf/*"]},
)
