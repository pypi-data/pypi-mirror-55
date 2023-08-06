import os
from setuptools import setup, find_packages

with open(os.path.join(os.getcwd(), "co2wui", "VERSION")) as version_file:
    version = version_file.read().strip()


def read(fpath):
    with open(fpath) as fp:
        return fp.read()


test_deps = ["pytest", "pytest-flask", "selenium"]
setup(
    name="co2wui",
    version=version,
    packages=find_packages(exclude=["test"]),
    license="European Union Public Licence 1.1 or later (EUPL 1.1+)",
    description="WebUI for co2mpas",
    long_description=read("README.md"),
    long_description_content_type="text/markdown; charset=UTF-8",
    keywords=["automotive", "vehicles", "simulator", "WLTP", "web-app"],
    url="https://github.com/JRCSTU/co2wui",
    project_urls={
        "Documentation": "https://co2mpas.io/",
        "Sources": "https://github.com/JRCSTU/co2wui",
    },
    python_requires=">=3.6",
    install_requires=[
        "co2mpas",
        "Flask",
        "Flask-Babel",
        "flask_session",
        "requests",
        "schedula",
        "Werkzeug",
        "click",
        "ruamel.yaml",
        "syncing",
        "urllib3",
    ],
    extras_require={
        "ta": ["co2mpas_dice"],
        "test": test_deps,
        "dev": test_deps
        + [
            "black",  # for code-formatting
            "pip",
            "pre-commit",  # for code-formatting
            "twine",
            "wheel",
        ],
    },
    entry_points={"console_scripts": ["co2wui=co2wui.app:cli"]},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Manufacturing",
        "Environment :: Console",
        "License :: OSI Approved :: European Union Public Licence 1.1 " "(EUPL 1.1)",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
)
