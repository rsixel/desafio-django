# !/bin/sh

cp Procfile_web Procfile

git commit -am "Procfile"
git push heroku master


heroku ps:scale web=1