import io
from setuptools import setup, find_packages

main_ns = {}
exec(open("dash_tokamak/version.py").read(), main_ns)  # pylint: disable=exec-used


def read_req_file(req_type):
    with open("requires-{}.txt".format(req_type)) as fp:
        requires = (line.strip() for line in fp)
        return [req for req in requires if req and not req.startswith("#")]

setup(
    name="dash_tokamak",
    version=main_ns["__version__"],
    author="Chris Parmer, Kevin Zeidler",
    author_email="",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    license="MIT",
    description=(
        """Dash without the annoying bits. Main goals of this fork are (1) to enable 
        Python to write state data to arbitrary component props, not just ones
        defined by a specific component; and (2) support React-style functional 
        property values by binding unary functional expressions to the global 
        application state, executing them whenever the property is accessed."""
    ),
    long_description=io.open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    install_requires=read_req_file("install"),
    extras_require={
        "dev": read_req_file("dev"),
        "testing": read_req_file("testing"),
    },
    entry_points={
        "console_scripts": [
            "dash_tokamak-generate-components = "
            "dash_tokamak.development.component_generator:cli",
            "renderer = dash_tokamak.development.build_process:renderer",
        ],
        "pytest11": ["dash_tokamak = dash_tokamak.testing.plugin"],
    },
    url="https://github.com/ProbonoBonobo/dash",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Dash",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Database :: Front-Ends",
        "Topic :: Office/Business :: Financial :: Spreadsheet",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Widget Sets",
    ],
)
