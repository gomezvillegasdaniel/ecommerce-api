## How to setup:

- sudo apt-get install python3-pip
- sudo pip3 install virtualenvwrapper

- Add theses lines to ~/.bashrc:
```
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Devel
export VIRTUALENVWRAPPER_VIRTUALENV=$(which virtualenv)
source /usr/local/bin/virtualenvwrapper.sh
```

- source ~/.bashrc:


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

- Add theses lines to ~/.bashrc:
```
export DATABASE_URL="postgres://username:password@host:port/dbname"
export FLASK_SECRET_KEY="secretkey"
```

- source ~/.bashrc
