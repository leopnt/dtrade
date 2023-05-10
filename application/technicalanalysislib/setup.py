from setuptools import find_packages, setup

setup(
    name="technicalanalysislib",
    packages=find_packages(include=["technicalanalysislib"]),
    version="0.1.0",
    description="A library to recognize ascending triangles in stock charts",
    author="Simon LEBOUCHER",
    licence="MIT",
    install_requires=[],
    setup_requires=["pytest-runner"],
    tests_require=["pytest==4.4.1"],
    test_suite="tests",
)
