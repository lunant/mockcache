from distutils.core import setup
from distutils.cmd import Command
from distutils import log
import re
import doctest
import mockcache


class test(Command):
    """Run unit tests."""

    description = __doc__
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        doctest.testmod(mockcache)


setup(name="mockcache",
      description="The Python dictionary-based mock memcached client library.",
      long_description=mockcache.__doc__,
      version=mockcache.__version__,
      author=mockcache.__author__,
      author_email=mockcache.__email__,
      maintainer=mockcache.__version__,
      maintainer_email=mockcache.__email__,
      url="http://bitbucket.org/lunant/mockcache/",
      py_modules=["mockcache"],
      cmdclass={"test": test},
      license=mockcache.__license__,
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Software Development :: Testing",
                   "Topic :: Software Development :: "
                   "Libraries :: Python Modules"])

