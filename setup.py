import setuptools

def readme():
    with open('README.rst') as f:
        return f.read()

setuptools.setup(
    name='atiiaftt',
    version='0.1.1',
    description="""CFFI wrap of ATI-IA force-torque sensor transform c library""",
    long_description=readme(),
    long_description_content_type="text/x-rst",
    url='https://github.com/shayden--/atiiaftt',
    download_url='https://github.com/shayden--/atiiaftt/tarball/0.1.1',
    author='Tyson Boer',
    author_email='ty@unutilized.net',
    license='MIT',
    packages=setuptools.find_packages(),
    include_package_data=True,
    setup_requires=["cffi>=1.0.0"],
    cffi_modules=["cffi_build.py:ffibuilder"],
    install_requires=["cffi>=1.0.0"],
    zip_safe=False,
    test_suite="nose.collector",
    tests_require=["nose"],
    keywords = ['ati','force','torque','sensor','instrumentation'],
    classifiers = [
        'Intended Audience :: Manufacturing',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        ],
    )
