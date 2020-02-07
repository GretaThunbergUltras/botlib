from setuptools import Extension, find_packages, setup

sonar_ext = Extension(
    'botlib.sonar',
    include_dirs = ['/usr/local/include'],
    libraries = ['wiringPi', 'pigpio', 'sonic'],
    sources = ['botlib/sonar/sonarmodule.c']
)

setup(
    name = 'botlib',
    version='0.0.2',
    packages = find_packages(),
    ext_modules = [sonar_ext]
)
