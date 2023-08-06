# from codecs import open
from os import path
from setuptools import find_packages, setup


here = path.abspath(path.dirname(__file__))

# Read requirements
requirements = [
    x.split("\n")[0]
    for x in open(path.join(here, "requirements.txt"), "r").readlines()[1:]
]

# Read README.md
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="simple-timebox",
    version="0.1",
    description="A simple countdown timer to boost effectiveness.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=["timebox", "time", "time management technique"],
    author="Stig-Ole Gundersen",
    author_email="stigole.gundersen@gmail.com",
    url="https://github.com/stigoleg/Timebox",
    license="MIT",
    packages=find_packages(),
    scripts=["timebox/app.py"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=requirements,
    entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      timebox = timebox.app:main
      """,
)
