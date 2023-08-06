from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='t-notes',
      version='0.1.0',
      description='Program for quick terminal-based notes',
      long_description=readme(),
      long_description_content_type='text/markdown',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
      ],
      keywords='notes terminal',
      url='http://github.com/oekshido/TNotes',
      author='oekshido',
      author_email='oekshido@gmail.com',
      license='MIT License',
      packages=['tnotes'],
      scripts=['bin/t', 'bin/tt', 'bin/tnotes'],
      install_requires=[
          'pyyaml',
          'readline',
      ],
      include_package_data=True,
      zip_safe=False)
