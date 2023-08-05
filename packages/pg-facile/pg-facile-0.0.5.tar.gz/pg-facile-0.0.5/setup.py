import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pg-facile", # Replace with your own username
    version="0.0.5",
    author="Pierre Grabolosa",
    author_email="pierre.grabolosa@imerir.com",
    description="An easy-to-use wrapper for psycopg2 for students.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pgrabolosa/pg-facile",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'psycopg2-binary',
    ],
    python_requires='>=3.6',
)
