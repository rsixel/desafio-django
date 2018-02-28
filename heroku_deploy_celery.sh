# !/bin/sh

cp Procfile_celery Procfile

git commit -am "Procfile"
git push heroku master


heroku ps:scale worker=1