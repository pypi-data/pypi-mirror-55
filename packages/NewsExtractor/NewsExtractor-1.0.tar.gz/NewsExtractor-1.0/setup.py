from setuptools import setup, find_packages

setup(
    name='NewsExtractor',
    packages=find_packages(),
    install_requires=['lxml', 'numpy'],
    version='1.0',
    description='General extractor of news pages.',
    author='RoryXiang',
    author_email='pingping19901121@gmail.com',
    url='',
    keywords=['python', 'webcrawler', 'webspider'],
    python_requires='>=3.6',
    license='RoryXiang',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    # zip_file=False

)
