# setup.py
from setuptools import setup, find_packages

setup(
    name="gracie-framework",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.19.0",
        "faiss-cpu>=1.7.0",
        "sentence-transformers>=2.2.0",
        "torch>=1.9.0",
        "sqlite3",
        "typing"
    ],
    author="Gracie Team",
    author_email="contact@gracie-ai.com",
    description="A Memetic Learning Framework for AI Agents",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gracie-ai/gracie-framework",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.8",
)
