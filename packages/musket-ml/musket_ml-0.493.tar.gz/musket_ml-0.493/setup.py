from setuptools import setup
import setuptools
setup(name='musket_ml',
      version='0.493',
      description='Common parts of my pipelines',
      url='https://github.com/petrochenko-pavel-a/musket_core',
      author='Petrochenko Pavel',
      author_email='petrochenko.pavel.a@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(),
      include_package_data=True,
      install_requires=["musket_text>=0.44","musket_core>=0.493","classification_pipeline>=0.431","segmentation_pipeline>=0.431"],
      zip_safe=False)