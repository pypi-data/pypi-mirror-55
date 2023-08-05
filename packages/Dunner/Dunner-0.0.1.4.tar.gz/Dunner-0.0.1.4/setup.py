
import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
   name='Dunner',
   version='0.0.1.4',
   author="Emre Begen",
   author_email="ebegen51@gmail.com",
   description="A helper package for data science projects",
   long_description=long_description,
   long_description_content_type="text/markdown",
   url="https://github.com/ebegen/Dunner",
   packages=setuptools.find_packages(),
   classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
   ],
   python_requires='>=3.7',
 )