from setuptools import setup, find_packages

setup(
    name="AnalyzeMCP",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.21.0',
        'pandas>=1.3.0',
        'scikit-learn>=0.24.2',
        'torch>=1.9.0',
        'transformers>=4.9.0',
        'fastapi>=0.68.0',
        'uvicorn>=0.15.0',
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A Machine Learning Control Protocol Analysis Tool",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/AnalyzeMCP",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)