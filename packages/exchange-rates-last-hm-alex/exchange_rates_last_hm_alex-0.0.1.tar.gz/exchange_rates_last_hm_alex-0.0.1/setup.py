from setuptools import setup, find_packages

with open("README.md", 'r') as file:
    long_desc = file.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="exchange_rates_last_hm_alex",
    version="0.0.1",
    author="BiggiPiggi",
    author_email="aszmey.war@gmail.com",
    description="Exchange rates getter",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ExampleUserForYandex/last",
    packages=find_packages(exclude=['test']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=required
)
