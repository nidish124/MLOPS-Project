from setuptools import setup, find_packages

def get_requirements()-> list:
    """Load requirements from a file."""
    requirements = []
    with open('requirements.txt', 'r') as file:
        read_line = file.readlines()
        for line in read_line:
            line = line.strip()
            if line and line not in ('- e'):
                requirements.append(line)

setup(
    name='MLOPS-Project',
    version='0.0.1',
    author='Nidish_M',
    author_email='nidish124@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements()
)