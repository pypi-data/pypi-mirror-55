from io import open
from setuptools import setup
from calamardolauncher import __version__ as version

setup(
    name='calamardolauncher',
    version=version,
    url='https://github.com/manso92/calamardolauncher',
    license='MIT',
    author='Pablo Manso',
    author_email='92manso@gmail.com',
    description='Compose Calamardo\'s params and launches the binary to generate files.',
    long_description=''.join(open('README.md', encoding='utf-8').readlines()),
    long_description_content_type='text/markdown',
    keywords=['gui', 'executable'],
    packages=['calamardolauncher'],
    include_package_data=True,
    install_requires=['Eel==0.10.4',
                      'google-api-python-client',
                      'google-auth-httplib2',
                      'google-auth-oauthlib'],
    python_requires='>=3.6',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux'
    ],
    entry_points={
        'console_scripts': [
            'calamardolauncher=calamardolauncher.__main__:run'
        ]
    }
)
