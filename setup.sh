set +ex

rm -rf env
virtualenv env
source env/bin/activate
pip install -r requirements.txt
