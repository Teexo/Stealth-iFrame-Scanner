from setuptools import setup, find_packages

setup(
    name="stealth_iframe_scanner",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Stealthy iframe SQL injection scanner with SQLmap integration",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/stealth-iframe-scanner",
    packages=find_packages(),
    install_requires=[
        "selenium>=4.0.0",
        "colorama>=0.4.4",
        "python-dotenv>=0.19.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Development Status :: 4 - Beta"
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "iframe-scanner=stealth_iframe_scanner:main",
        ],
    },
)
