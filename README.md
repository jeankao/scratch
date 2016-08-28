# scratch

```
heroku create <scratchweb> --buildpack https://github.com/kennethreitz/conda-buildpack

heroku git:remote -a <scratchweb>          

heroku config:set DJANGO_SETTINGS_MODULE=scratch.production_settings

heroku config:add BUILDPACK_URL=https://github.com/kennethreitz/conda-buildpack.git

heroku addons:create heroku-postgresql

git push heroku master

heroku run python manage.py makemigrations

heroku run python manage.py migrate

heroku run python manage.py createsuperuser

heroku logs --app <scratchweb>   
```