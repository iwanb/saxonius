#!/usr/bin/env python
"""Python bindings for Saxon, using pyJNIus
"""
doclines = __doc__.split("\n")

classifiers = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
License :: OSI Approved :: Apache Software License
Operating System :: POSIX
Operating System :: Microsoft :: Windows
Operating System :: Unix
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 3
Topic :: Text Processing :: Markup :: XML
Topic :: Software Development :: Libraries :: Python Modules
"""
try:
    from setuptools import setup
    pass
except:
    from distutils.core import setup
    pass

setup(
    name="saxonius",
    version="1.0",
    author="Iwan Briquemont",
    author_email="tracnar@gmail.com",
    url="https://github.com/iwanb/saxonius",
    packages=['saxonius'],
    keywords=["xml", "xquery", "saxon"],
    license="http://www.apache.org/licenses/LICENSE-2.0",
    description=doclines[0],
    long_description="\n".join(doclines[2:]),
    requires=["jnius"],
    test_suite="tests",
)
