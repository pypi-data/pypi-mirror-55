import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()
# name = roomservice

setuptools.setup(
    name="roomservice",
    version="0.0.7",
    author="Rory Murdock",
    author_email="rmurdock@woolworths.com.au",
    description="A Library for interacting with Google Sheets, changing your sheets",
    # long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/rorymurdock/WSO-UEM-Py",
    packages=setuptools.find_packages(),
    classifiers=[
        # "Development Status :: 5 - Production/Stable",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'google-auth-httplib2',
          'google-api-python-client',\
    ]
)