from setuptools import setup

setup(
   name='sertis',
   version='1.0',
   description='A useful module (for testing)',
   license="MIT",
   long_description=long_description,
   author='Man Foo',
   author_email='foomail@foo.com',
   url="http://www.foopackage.com/",
   packages=['thainlplib'],  #same as name
   package_data={"thainlplib": ["saved_model/**/*"]},

)