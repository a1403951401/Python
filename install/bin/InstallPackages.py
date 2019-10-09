import os
from .func import sh

def install(path):
    list = os.listdir(f'{path}/download/')
    for i in list:
        if i[-4:] == ".whl":
            sh(f"pip install --no-index --find-links={path}/download/ {i}")

