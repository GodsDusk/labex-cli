from setuptools import setup, find_packages

setup(
    name="labex",
    version="0.0.2",
    description="LabEx CLI",
    author="huhuhang",
    author_email="huhuhang@gmail.com",
    url="https://github.com/labex-labs/labex-cli",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">3.8.0",
    install_requires=[
        "Click",
        "rich",
        "PyGithub",
        "GitPython",
        "jsonschema",
        "pandas",
        "retrying",
        "openai >= 1.3",
        "titlecase",
        "langchain",
        "tiktoken",
        "requests_toolbelt",
    ],
    entry_points="""
        [console_scripts]
        labex=labex.cli:cli
    """,
)
