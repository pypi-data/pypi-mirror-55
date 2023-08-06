import setuptools

setuptools.setup(
    name='esy-osm-pbf',
    description='Low-level interface to OpenStreetMap protocol buffer files.',
    version='0.0.1',
    license='GPLv3',
    long_description=open('doc/index.rst', 'r').read(),
    long_description_content_type='text/x-rst',
    author='Ontje Lünsdorf',
    author_email='ontje.luensdorf@dlr.de',
    package_dir={'': 'src'},
    packages=setuptools.find_namespace_packages(where='src'),
    python_requires='>= 3.5',
    install_requires=['protobuf >= 3, < 4'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        (
            'License :: OSI Approved :: '
            'GNU General Public License v3 or later (GPLv3+)'
        ),
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
    ],
)
