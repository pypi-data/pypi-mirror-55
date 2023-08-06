import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='sighthound_api',
     version='0.62',
     author="Phil Mottin",
     author_email="philmottin@gmail.com",
     description="Sighthound API for integration with Home Assistant",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/philmottin",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
