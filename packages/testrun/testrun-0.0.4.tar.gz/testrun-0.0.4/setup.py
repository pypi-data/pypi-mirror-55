import setuptools

with open('README.md') as fh:
    long_description = fh.read()

setuptools.setup(
    name='testrun',
    version='0.0.4',
    author='ES-Alexander',
    auther_email='sandman.esalexander@gmail.com',
    description='A package for tests with meaningful output and display (IDLE-Compatible)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ES-Alexander/testrun',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
