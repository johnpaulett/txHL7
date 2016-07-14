from setuptools import setup

setup(
    name='txHL7',
    version='0.4.1',
    author='John Paulett',
    author_email='john@paulett.org',
    description="""
    Async Twisted server implementation of Health Level 7's (HL7)
    Minimal Lower-Layer Protocol (MLLP).
    """,
    url='http://txHL7.readthedocs.org',
    license='BSD',
    platforms=['POSIX', 'Windows'],
    keywords=['HL7', 'Health Level 7', 'healthcare', 'health care',
              'medical record', 'twisted'],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Framework :: Twisted',
        'Intended Audience :: Developers',
        'Intended Audience :: Healthcare Industry',
        'Topic :: Communications',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking'
    ],
    packages=['txHL7', 'twisted.plugins'],
    package_data={
        "twisted": ["plugins/mllp_plugin.py"]
    },
    install_requires=[
        # require twisted, but allow client to require specific version
        'twisted',
        'hl7>=0.3.1',
        'six',
    ],
)
