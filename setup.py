"""
Setup script for Vantage AI PersonaPilot
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="vantage-ai-personapilot",
    version="1.0.0",
    author="Vantage AI Team",
    author_email="team@vantage-ai.com",
    description="Persona-driven AI assistant powered by Generative AI",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/vantage-ai/personapilot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "web": [
            "fastapi>=0.104.0",
            "uvicorn>=0.24.0",
            "jinja2>=3.1.0",
        ],
        "rag": [
            "sentence-transformers>=2.2.0",
            "faiss-cpu>=1.7.0",
            "numpy>=1.24.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "vantage-ai=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.json"],
    },
    keywords="ai, persona, chatbot, generative-ai, rag, prompt-engineering",
    project_urls={
        "Bug Reports": "https://github.com/vantage-ai/personapilot/issues",
        "Source": "https://github.com/vantage-ai/personapilot",
        "Documentation": "https://vantage-ai.github.io/personapilot/",
    },
)

