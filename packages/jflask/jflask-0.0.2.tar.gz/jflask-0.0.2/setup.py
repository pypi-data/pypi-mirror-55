from setuptools import setup


def get_requirements():
    with open('requirements.txt') as fp:
        return fp.readlines()


def get_version():
    with open('.version') as fp:
        return fp.read()

setup(
    name='jflask',
    version=get_version(),
    packages=['jflask'],
    url='https://github.com/jfudally/jflask',
    license='MIT',
    author='jfudally',
    author_email='justinfudally@gmail.com',
    description='JSON flask helpers',
    install_requires=get_requirements(),
    python_requires='>=3.6'
)
