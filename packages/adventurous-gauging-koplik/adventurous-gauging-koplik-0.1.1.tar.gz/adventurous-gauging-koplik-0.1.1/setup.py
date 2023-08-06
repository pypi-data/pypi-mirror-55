import setuptools

with open('README.md','r') as fh:
	long_description = fh.read()

setuptools.setup(name='adventurous-gauging-koplik',
	  version = '0.1.1',
	  description = 'Decription',
	  long_description = long_description,
	  long_description_content_type = 'text/markdown',
	  url='http://github.com/kshamruk/adventurous-gauging-koplik',
	  author = 'kshamruk',
	  author_email = 'c.shamruk@gmail.com',
	  license='MIT',
	  packages=setuptools.find_packages(),
	  classifiers = [
	  			'Programming Language :: Python :: 3',
	  			'License :: OSI Approved :: MIT License',
	  			'Operating System :: OS Independent',
	  			],
	  install_requires = ['scipy','numpy','opencv-python',
	  'torch','numba','efficientnet_pytorch','tqdm'],
	  python_requires = '>=3.6')