from setuptools import setup

setup(
    name='twisted-hl7',
    version='0.0.1',
    author='John Paulett',
    author_email = 'john@paulett.org',
    url = 'http://github.com/johnpaulett/twisted-hl7',
    license = 'BSD',
    platforms = ['POSIX', 'Windows'],
    keywords = ['HL7', 'Health Level 7', 'healthcare', 'health care',
                'medical record', 'twisted'],
    classifiers = [
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Healthcare Industry',
        'Topic :: Communications',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages = ['twistedhl7'],
    # require twisted, but allow client to require specific version
    install_requires = ['twisted'],
)
