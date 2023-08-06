from setuptools import setup, find_packages

with open('sxyz/requirements.txt') as fp:
    requires = [l.strip() for l in fp.readlines() if l]

with open('README.md') as f:
    long_description = f.read()

setup(
    name='sxyz',
    version='0.1',
    author='edgesider',
    author_email='yingkaidang@gmail.com',
    description='Sxyz',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/edgesider/sxyz',

    packages=find_packages(),
    install_requires=requires,
    python_requires='>=3.5',

    entry_points={
        'console_scripts': ['sxyz = sxyz.sxyz:main']
    }
)
