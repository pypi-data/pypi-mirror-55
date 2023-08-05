from setuptools import setup

setup(name='gcluster',
      version='0.0.1a0',
      description='Clustering based on graph algorithms',
      long_description='Clustering based on graph algorithms',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
      ],
      keywords='graph clustering',
      url='http://github.com/lucifer1004/gcluster',
      author='Gabriel Wu',
      author_email='wuzihua@pku.edu.cn',
      license='MIT',
      packages=['gcluster'],
      install_requires=[],
      include_package_data=True,
      zip_safe=False)
