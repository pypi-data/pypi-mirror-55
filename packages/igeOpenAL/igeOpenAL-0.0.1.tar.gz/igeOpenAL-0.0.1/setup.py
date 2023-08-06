import importlib
try:
    importlib.import_module('numpy')
except ImportError:
	from pip._internal import main as _main
	_main(['install', 'numpy'])

from setuptools import setup, Extension, find_packages
import setuptools
import numpy
import sys
import os
from distutils.sysconfig import get_python_lib
import shutil

# To use a consistent encoding
from codecs import open

from os import path
here = path.abspath(path.dirname(__file__))

is64Bit = sys.maxsize > 2 ** 32
bindir = ''
if is64Bit:
    bindir = 'bin/win64'
else:
    bindir = 'bin/win32'

shutil.copy2(bindir+'/OpenAL32.dll', 'igeOpenAL')

sfc_module = Extension('igeOpenAL.igeOpenAL',
                    sources=[
                        'pyxOpenAL.cpp',
                        'OpenAL.cpp',
                    ],
                    include_dirs=['bin/include'],
                    library_dirs=[bindir],
			        libraries=['OpenAL32', 'ogg', 'vorbis', 'vorbisfile'])

setup(name='igeOpenAL', version='0.0.1',
		description='C++ extension OpenAL sound for 3D and 2D games.',
		author=u'Indigames',
		author_email='dev@indigames.net',
		packages=find_packages(),
		ext_modules=[sfc_module],
		long_description=open(path.join(here, 'README.md')).read(),
        long_description_content_type='text/markdown',
        
        # The project's main homepage.
        url='https://indigames.net/',
        
		license='MIT',
		classifiers=[
			'Intended Audience :: Developers',
			'License :: OSI Approved :: MIT License',
			'Programming Language :: Python :: 3',
			#'Operating System :: MacOS :: MacOS X',
			#'Operating System :: POSIX :: Linux',
			'Operating System :: Microsoft :: Windows',
			'Topic :: Games/Entertainment',
		],
        #data_files=[
        #    ('Lib/site-packages/pyxie', [bindir+"/pyxcore.dll"]),
        #    ('Lib/site-packages/pyxie/devtool',  [bindir+"/pyxtools.dll", bindir+"/PVRTexLib.dll"])
        #],
        
        # What does your project relate to?
        keywords='OpenAL 3D game Xiph ogg vorbis opus sound playback audio indigames',
    
		package_data={'igeOpenAL': ['*.dll']},        
        include_package_data=True
      )
