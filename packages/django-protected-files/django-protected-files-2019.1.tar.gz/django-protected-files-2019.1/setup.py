from setuptools import setup, find_packages

setup(name='django-protected-files',
      version='2019.1',
      description='Simple django protected media and static',
      packages=find_packages(),
      install_requires=[
        'django>=2.2.3',
      ],
      include_package_data=True,
      zip_safe=False)
