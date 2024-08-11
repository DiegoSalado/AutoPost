from setuptools import find_packages, setup

setup(
    name="instagram_post",
    packages=find_packages(exclude=["instagram_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "pandas",
        "dbt-core",
        "psycopg2-binary",
    ],
    extras_require={"dev": ["dagit", "pytest", "localstack"]},
)
