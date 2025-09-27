from setuptools import setup, find_packages

setup(
    name="pyrsing",
    version="0.1.0",
    description="A Python parsing library.",
    author="samuelcorradi",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
    python_requires=">=3.7",
)