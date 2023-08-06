from setuptools import setup

VERSION = '1.0.0'

setup(
    name='ics_ipa_interface',
    packages=['ics_ipa_interface'],
    version=VERSION,
    description='API used to to allow users to make scripts that work local'
                ' and on wivi server',
    long_description='This project is designed to allow users of IPA to seamlessly \
                      transition between Desktop and WiVi.',
    maintainer='Zaid Nackasha',
    maintainer_email='ZNackasha@intrepidcs.com',
    url='https://github.com/intrepidcs/ics_ipa_interface',
    download_url='https://github.com/intrepidcs/ics_ipa_interface/archive/' +
                 VERSION + '.tar.gz',
    classifiers=['Operating System :: Microsoft :: Windows',
                 'Operating System :: Unix',
                 'Programming Language :: Python :: 3.6']
)

