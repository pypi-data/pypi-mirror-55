import setuptools 

setuptools.setup(
    name='netsdldv',
    version='0.0.2',
    description='a tools for ami',
    url='https://git.netsdl.com/dv/DvManager',
    author='codmowa',
    author_email='chenchu@netsdl.com',
    license='MIT',
    keywords='ami dv python',
    package_dir={'':'.'},
    install_requires=['pyodbc >= 4.0.27','SQLAlchemy >= 1.3.11'],
    packages=setuptools.find_namespace_packages(exclude=["*test*"])
)