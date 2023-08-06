import setuptools
from distutils.core import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='testkernel',
    version='1.6.1',
    url='https://github.com/',
    author="test",
    author_email="test@gmail.com",
    long_description=readme,
    setup_requires=["wheel"],
    packages=['kernels', 'kernels/att_kernel', 'kernels/intel_kernel', 'kernels/riscv_kernel', 'assembler', 'assembler/Intel', 'assembler/RISCV'],
)
