"""新闻聚合器包配置"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="news-aggregator",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="自动化新闻聚合器 - 每日获取科技、财经、娱乐新闻",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/news-aggregator",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="news aggregator rss python github-actions automation",
    project_urls={
        "Bug Reports": "https://github.com/your-username/news-aggregator/issues",
        "Source": "https://github.com/your-username/news-aggregator",
    },
    entry_points={
        "console_scripts": [
            "news-aggregator=main:main",
        ],
    },
)