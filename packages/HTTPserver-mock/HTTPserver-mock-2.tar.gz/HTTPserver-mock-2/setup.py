from setuptools import setup

with open('README.md', 'r') as fp:
    long_desc = fp.read()

setup(
    name='HTTPserver-mock',
    version='2',
    author='Tom YU Choe',
    author_email='yonguk.choe@gmail.com',
    description='a simple http-server mockup to test web crawler.',
    long_description=long_desc,
    url='https://github.com/YUChoe/noizze_crawler',
    long_description_content_type="text/markdown",
    py_modules=['HTTPserver_mock'],
    package_dir={'': 'src'},
    license='MIT',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=[],
)
