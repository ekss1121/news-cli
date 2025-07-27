from setuptools import setup, find_packages

setup(
    name="f1-news-cli",
    version="0.1.0",
    description="CLI tool to fetch F1 news from social media",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "feedparser>=6.0.0",
        "rich>=13.0.0",
        "requests>=2.28.0",
        "python-dateutil>=2.8.0",
    ],
    entry_points={
        "console_scripts": [
            "f1-news=f1_news.cli:main",
        ],
    },
    python_requires=">=3.8",
)