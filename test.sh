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

source $SCRIPTPATH/activate

python src/pyck/test/test.py