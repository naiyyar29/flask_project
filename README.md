# flask_project
1)Install and activate Python environment
pip install venv
python venv -m venv

2)Activate the environment
.\venv\Scripts\activate.ps1

3)in the environment download flask,flask-sqlalchemy,stripe

pip install flask
pip install Flask-SQLALchemy
pip install stripe

4)create a database

in the venv go to
python
from app import db
db.create_all()

database will be created

5)run the app.py

python app.py
