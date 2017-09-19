# Get virtualenv
rm -rf virtualenv*
curl --silent --show-error -o virtualenv.tar.gz https://pypi.python.org/packages/c8/82/7c1eb879dea5725fae239070b48187de74a8eb06b63d9087cd0a60436353/virtualenv-15.0.1.tar.gz
tar xvf virtualenv.tar.gz > /dev/null

# Prepare env
rm -rf env
python virtualenv-15.0.1/virtualenv.py env
source env/bin/activate
pip install -r requirements.txt
