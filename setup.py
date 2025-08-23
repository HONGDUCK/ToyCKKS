from setuptools import setup, find_packages

setup(
    name="ToyCKKS",
    version="0.1.0",
    description="ToyCKKS",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.20",
    ],
    python_requires=">=3.10",
)
