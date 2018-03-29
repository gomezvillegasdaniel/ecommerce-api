## How to setup:

- install these packages
```
sudo apt-get install python3 python3-pip python3-virtualenv
sudo pip3 install virtualenvwrapper
```

- Add these environment variables to ~/.bashrc substituting your own db config
```
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_VIRTUALENV=$(which virtualenv)
source /usr/local/bin/virtualenvwrapper.sh
export DATABASE_URL="postgres://username:password@host:port/dbname"
export FLASK_SECRET_KEY="secretkey"
```
- apply them
```
source ~/.bashrc
```

- execute
```
mkvirtualenv -p python3 ecommerce_api_venv
workon ecommerce_api_venv
pip3 install -r requirements.txt

sudo apt-get install postgresql postgresql-contrib libpq-dev
sudo -i -u postgres
psql -c "CREATE ROLE username LOGIN ENCRYPTED PASSWORD 'password' CREATEDB VALID UNTIL 'infinity';"
sudo /etc/init.d/postgresql restart
createdb dbname
```

- add this line to ~/.bashrc for production purposes only
```
export ENV="PROD"
```
- apply
```
source ~/.bashrc
```
