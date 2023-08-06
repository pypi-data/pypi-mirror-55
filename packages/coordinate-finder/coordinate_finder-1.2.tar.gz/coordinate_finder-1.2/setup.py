from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="coordinate_finder",
    version="1.2",
    author="Alex Terry & Alistair Heath",
    author_email="alexterry48@gmail.com.com",
    description="Package to find equidistant Lat & Long coordinates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Alexterry101/MarsCoordFinder",
    packages=['coordinate_finder'],
    install_requires=[
          'scikit_learn',
          'pandas',
          'matplotlib',
          'numpy',
    ],
    classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    zip_safe=False,
    include_package_data=True)
