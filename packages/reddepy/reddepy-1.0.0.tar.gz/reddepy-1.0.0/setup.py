from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="reddepy",
    version="1.0.0",
    description="A Python package that allows merchants to receive, send, check transaction status, and perform lots of payment transactions using Redde payment API.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/wigalsolutionsltd/reddePy",
    author="Richard Asante",
    author_email="ricardo.volvox@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["reddepy"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "",
        ]
    },
)
