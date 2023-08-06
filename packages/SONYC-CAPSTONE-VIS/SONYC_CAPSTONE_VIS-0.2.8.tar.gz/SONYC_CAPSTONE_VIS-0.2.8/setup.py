from setuptools import setup, find_packages

setup(
    name='SONYC_CAPSTONE_VIS',
    version='0.2.8',
    keywords=['SONYC', 'visualization'],
    description='SONYC Capstone Visualization Pacakge',
    long_description='',
    license='MIT',
    install_requires=["matplotlib", "numpy", "pandas", "umap", "sklearn", "h5py"],
    author='Biao',
    author_email='biaoh66@gmail.com',
    packages=find_packages(),
    platforms='any',
    url='https://github.com/Distancs/SONYC_CAPSTONE_VIS'
)
