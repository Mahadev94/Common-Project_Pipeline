from setuptools import setup,find_packages
from typing import List
file_path="requirements.txt"
HYPEN_E_DOT="-e ."

def get_requirements(file_path:str)->List[str]:
    requirements=[]
    with open(file_path) as file_obj:
        requiremets=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return requirements

setup(
    name="House-Price",
    version="0.0.1",
    author="Mahadev94",
    author_emial="mahadev.mk294@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(file_path)
)