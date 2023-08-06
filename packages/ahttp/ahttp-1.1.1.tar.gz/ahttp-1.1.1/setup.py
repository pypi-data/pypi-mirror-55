from setuptools import setup, find_packages, os

setup(
	name='ahttp',
	version='1.1.1',
	description='Based on aiohttp and asyncio requests',
    long_description='The Instructions of ahttp at https://github.com/web-trump/ahttp.git',
	install_requires=['aiohttp>=3.6.2', 'cchardet>=2.1.4', "requests_html>=0.10.0"] ,
	author='LiShenGang',
	author_email='cszy2013@163.com',
	license='BSD License',
	py_modules= ['ahttp'] ,
	platforms=["python 3.7"],
	url='https://github.com/web-trump/ahttp.git',
	classifiers=[
		'Development Status :: 6 - Mature',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3.7',
		],
)