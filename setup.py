from setuptools import setup, find_packages

setup(
    name="makemerich",
    version="0.1.0",
    description="The AI that actually makes you money — autonomous crypto trading agent",
    author="E. Weil",
    url="https://github.com/e-weil/makemerich",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0",
        "pydantic>=2.0",
        "ccxt>=4.0",
        "python-binance>=1.0.19",
        "anthropic>=0.40.0",
        "pandas>=2.0",
        "numpy>=1.24",
        "ta>=0.11.0",
        "fastapi>=0.110.0",
        "uvicorn>=0.27.0",
        "jinja2>=3.1",
        "structlog>=24.0",
        "rich>=13.0",
    ],
    entry_points={
        "console_scripts": [
            "makemerich=makemerich.main:main",
        ],
    },
    license="MIT",
)
