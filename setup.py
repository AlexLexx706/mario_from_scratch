from setuptools import setup, find_packages

setup(
    name='mario',
    version='0.0.0',
    author='akalmykov',
    author_email='alexlexx1@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mario = mario:main',
        ],
    },
    package_data={
        'mario': [
            'images/*',
        ]
    }
)
