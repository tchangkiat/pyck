#!/bin/bash

echo Creating virtual environment...
python3 -m venv pyck-env

echo Virtual environment created at `pwd`/pyck-env

echo "OS is $OSTYPE";

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    SCRIPTPATH=pyck-env/bin
elif [[ "$OSTYPE" == "darwin"* ]]; then
    SCRIPTPATH=pyck-env/bin
elif [[ "$OSTYPE" == "cygwin" ]]; then
    SCRIPTPATH=pyck-env/Scripts
elif [[ "$OSTYPE" == "msys" ]]; then
    SCRIPTPATH=pyck-env/Scripts
elif [[ "$OSTYPE" == "win32" ]]; then
    SCRIPTPATH=pyck-env/Scripts
else
    echo "Couldn't find activate script.";
    exit 1;
fi

echo "Activating virtual environment"
source $SCRIPTPATH/activate

python -m pip install -e .

echo "Done"