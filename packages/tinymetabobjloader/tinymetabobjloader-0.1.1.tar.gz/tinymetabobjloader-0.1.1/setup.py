import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# Adapted from https://github.com/pybind/python_example/blob/master/setup.py
class get_pybind_include(object):
    """Helper class to determine the pybind11 include path
    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __init__(self, user=False, pep517=False):
        self.user = user
        self.pep517 = pep517

    def __str__(self):
        import os
        import pybind11

        interpreter_include_path = pybind11.get_include(self.user)

        if self.pep517:
            # When pybind11 is installed permanently in site packages, the headers
            # will be in the interpreter include path above. PEP 517 provides an
            # experimental feature for build system dependencies. When installing
            # a package from a source distribvution, first its build dependencies
            # are installed in a temporary location. pybind11 does not return the
            # correct path for this condition, so we glom together a second path,
            # and ultimately specify them _both_ in the include search path.
            # https://github.com/pybind/pybind11/issues/1067
            return os.path.abspath(
                os.path.join(
                    os.path.dirname(pybind11.__file__),
                    "..",
                    "..",
                    "..",
                    "..",
                    "include",
                    os.path.basename(interpreter_include_path),
                )
            )
        else:
            return interpreter_include_path


# `tiny_obj_loader.cc` contains implementation of tiny_obj_loader.
m = setuptools.Extension(
    "tinyobjloader",
    extra_compile_args=["-std=c++11"],
    sources=["bindings.cc", "tiny_obj_loader.cc"],
    include_dirs=[
        # Support `build_ext` finding tinyobjloader (without first running
        # `sdist`).
        "..",
        # Support `build_ext` finding pybind 11 (provided it's permanently
        # installed).
        get_pybind_include(),
        get_pybind_include(user=True),
        # Support building from a source distribution finding pybind11 from
        # a PEP 517 temporary install.
        get_pybind_include(pep517=True),
    ],
    language="c++",
)


setuptools.setup(
    name="tinymetabobjloader",
    version="0.1.1",
    description="Experimental fork of tinyobjloader Python module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Syoyo Fujita, Paul Melnikow",
    author_email="syoyo@lighttransport.com, github@paulmelnikow.com",
    url="https://github.com/metabolize/tinyobjloader",
    classifiers=["License :: OSI Approved :: MIT License"],
    packages=setuptools.find_packages(),
    ext_modules=[m],
)
