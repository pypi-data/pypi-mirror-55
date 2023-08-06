import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="personal-page-creator",
    version="0.0.13",
    author="Udith Prabhu",
    author_email="udithprabhu@gmail.com",
    description="Script to generate static page for GitHub pages.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/udithprabhu/personal-page-creator",
    packages=["personal_page_creator"],
    package_dir={"personal_page_creator": "personal_page_creator"},
    install_requires=['requests', "Jinja2"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'ppc=personal_page_creator.__main__:main'
        ]
    },
    package_data = {"personal_page_creator": ["templates/*"]},
    python_requires='>=3.4',
)