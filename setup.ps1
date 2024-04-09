echo "Creating virtual environment..."
python3 -m venv pyck-env

.\pyck-env\Scripts\activate

.\pyck-env\Scripts\python.exe -m pip install -e .

echo "Done"