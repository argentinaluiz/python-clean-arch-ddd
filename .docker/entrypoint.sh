#!/bin/bash

cd src/__core
pdm install
cd ../..

cd src/django_app
pdm install
cd ../..

#remover porque não precisa já tem no .bashrc
#eval "$(pdm --pep582)"

tail -f /dev/null

# make runserver