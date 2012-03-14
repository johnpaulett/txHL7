from setuptools import setup

setup(
    name='twisted-hl7',
    version='0.0.3',
    author='John Paulett',
    author_email = 'john@paulett.org',
    url = 'http://twisted-hl7.readthedocs.org',
    license = 'BSD',
    platforms = ['POSIX', 'Windows'],
    keywords = ['HL7', 'Health Level 7', 'healthcare', 'health care',
                'medical record', 'twisted'],
    classifiers = [
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
    packages = ['twistedhl7'],
    install_requires = [
        # require twisted, but allow client to require specific version
        'twisted',
        'hl7'
    ],
)
