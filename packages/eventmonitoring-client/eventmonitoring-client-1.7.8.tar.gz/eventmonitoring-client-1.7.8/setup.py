from setuptools import setup, find_packages

setup(
    name="eventmonitoring-client",
    version="1.7.8",
    packages=find_packages(),
    install_requires=["requests>=2.18.2", "zappa>=0.47.1"],
)
