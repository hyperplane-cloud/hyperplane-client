import setuptools
from setuptools.command.build_py import build_py
import os


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Known Issue: When uninstalling on windows the tons.cmd will remain
class CustomPythonBuild(build_py):
    def add_to_win_path(self):
        try:
            win_dir = os.environ.get('LOCALAPPDATA')
            if not win_dir:
                return
            fp = os.path.join(win_dir, "Microsoft", "WindowsApps", "tons.cmd")
            with open(fp, 'wt') as f:
                f.write("@python3 -m tons_cli %*")
        except BaseException as e:
            pass

    def run(self):
        if os.name == 'nt':
            self.execute(self.add_to_win_path, ())
        build_py.run(self)


setuptools.setup(
    name="hyperplane",
    version="0.0.3",
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
    install_requires=['requests', 'click'],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'tons = tons_cli.__main__:main',
        ]
    },
    cmdclass={'build_py': CustomPythonBuild},
)
