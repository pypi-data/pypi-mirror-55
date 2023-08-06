import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jintian-architecture-code-test",
    version="1.0",
    author="",
    author_email="767980702@qq.com",
    description="jintian-architecture-code",
    long_description=long_description,
    include_package_data=True,
    long_description_content_type="",
    url="",
    packages=['com/fw/base', 'com/fw/db', 'com/fw/system','com/fw/utils', 'com/fw/routes'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
