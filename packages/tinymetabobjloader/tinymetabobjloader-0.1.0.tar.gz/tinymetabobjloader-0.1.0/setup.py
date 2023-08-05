import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# https://github.com/pybind/python_example/blob/master/setup.py
class get_pybind_include(object):
    """Helper class to determine the pybind11 include path
    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11

        return pybind11.get_include(self.user)


# `tiny_obj_loader.cc` contains implementation of tiny_obj_loader.
m = setuptools.Extension(
    "tinyobjloader",
    extra_compile_args=["-std=c++11"],
    sources=["bindings.cc", "tiny_obj_loader.cc"],
    include_dirs=[
        # Make `build_ext` work without `sdist`.
        "..",
        # Support `build_ext` as well as installs from source distribution.
        get_pybind_include(),
        get_pybind_include(user=True),
    ],
    language="c++",
)


setuptools.setup(
    name="tinymetabobjloader",
    version="0.1.0",
    description="Experimental fork of tinyobjloader Python module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Syoyo Fujita, Paul Melnikow",
    author_email="syoyo@lighttransport.com, github@paulmelnikow.com",
    url="https://github.com/metabolize/tinyobjloader",
    classifiers=["License :: OSI Approved :: MIT License"],
    packages=setuptools.find_packages(),
    install_requires=["pybind11>=2.3"],
    setup_requires=["pybind11>=2.3"],
    ext_modules=[m],
)
