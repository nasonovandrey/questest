from setuptools import find_packages, setup

setup(
    name="questest",
    version="0.1",
    packages=find_packages(),
    scripts=["questest.py"],
    install_requires=["pytest==7.2.2", "ipytest==0.14.0"],
    entry_points={"console_scripts": ["questest=questest.main"]},
    author="Andrei Nasonov",
    author_email="andrey.m.nasonov@gmail.com",
    description="Utility to run pytest with optional breakpoint insertion ",
    url="https://github.com/nasonovandrey/questest",
    license="BSD",
)
