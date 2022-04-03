import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hyperplane",
    version="0.0.2",
    author="Hyperplane",
    author_email="adam@hyperplane.cloud",
    description="A client-code facing library exposing internal APIs for the Hyperplane.cloud platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='This code is property of Hyperplane, all rights reserved, do not distribute',
    url="https://dev.hyperplane.cloud",
    project_urls={
        "Bug Tracker": "https://github.com/hyperplane-cloud/hyperplane-dev/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: GPU",  # Environment :: GPU :: NVIDIA CUDA :: 11.3
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=['requests'],
    python_requires=">=3.6",
)
