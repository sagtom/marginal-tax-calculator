from setuptools import setup, find_packages

setup(
    name="marginal_tax_calculator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "pydantic",
        "requests",
        "pydantic-settings",
        "python-dotenv"
    ],
)
