from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='api_res_py',
      version='0.1',
      description='AS api response python package',
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Topic :: Text Processing :: Linguistic',
      ],
      keywords='as api res',
      url='https://github.com/rakeshrkz7/as_api_res',
      author='Rakesh',
      author_email='rakesh.r@payoda.com',
      license='MIT',
      packages=['api_res_py'],
      dependency_links=['https://github.com/rakeshrkz7/as_api_res/master#egg=package-1.0'],
      install_requires=[
          'request',
      ],
      include_package_data=True,
      zip_safe=False)
