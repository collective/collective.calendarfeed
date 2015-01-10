python setup.py sdist --formats=zip
cp dist/*.zip ../../heroku-deploy/pypi_local/
cd ../../heroku-deploy/
git commit -am 'updated theme'
git add -A
git commit -am 'updated theme'
git push heroku master
