from setuptools import find_packages, setup, Extension
import numpy

tricube_cpp_module = Extension(
    'mff.interpolation.tricube_cpp._tricube',
    sources=["mff/interpolation/tricube_cpp/tricube_module.c", "mff/interpolation/tricube_cpp/_tricube.c"],
    include_dirs=[numpy.get_include(), "mff/interpolation/tricube_cpp/"]
)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mff',
    version='0.2.3',
    author='Claudio Zeni, Adam Fekete, Aldo Glielmo',
    author_email='claudio.zeni@kcl.ac.uk',
    description='Gaussian process regression to extract non-parametric 2- and 3- body force fields.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kcl-tscm/mff",
    packages=find_packages(),
    ext_modules=[tricube_cpp_module],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'asap3',
        'ase',
        'theano >= 1.0.4',
        'scipy'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Scientific/Engineering :: Physics'
    ],
)
