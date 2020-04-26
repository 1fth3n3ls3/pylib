import os
import sys

# append vanilla python site-packages
sys.path.append('C:\Python27\Lib\site-packages')

# import your module
import pylib.utils
reload(pylib.utils)
# import nose
import nose
# create an instance of a test loader
# a test loader is responsible for discovering tests
testLoader = nose.loader.TestLoader()
# load the tests from our module
testSuite = testLoader.loadTestsFromModule(pylib)
# run them
nose.run(suite=testSuite, argv=["--with-cov",  "--cover-package=pylib"])

