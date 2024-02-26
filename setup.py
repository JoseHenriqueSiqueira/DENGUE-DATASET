from setuptools import setup

with open('README.md', 'r', encoding='UTF-8') as file:
    readme = file.read()

setup(name='API-DENGUE',
    version='0.0.1',
    license='MIT License',
    author='José Henrique da Silva Siqueira',
    long_description=readme,
    long_description_content_type='text/markdown',
    keywords='dengue dengue-api dengue api',
    description='Api dengue 2024',
    packages=['dengue_api'],
    install_requires=['requests']
    )