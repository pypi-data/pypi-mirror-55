from pathlib import Path
from setuptools import setup, find_packages

HERE = Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="caesium-lang",
    version="1.0.0",
    packages=find_packages(),
    description="A simple way to evaluate Boolean Algebra.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Armani-T/Caesium",
    author="Armani Tallam",
    author_email="armanitallam@gmail.com",
    license="BSD License",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Typing :: Typed",
    ],
    install_requires=["typing"],
    entry_points={
        "console_scripts": [
            "caesium=caesium:main",
        ]
    },
)
