# holistiplan-be

# Start Django
Create your venv:
```
pip install virtualenv
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Start django
```
./manage.py 
./manage.py migrate
./manage.py runserver
```

I would usually not include the venv, but 


# Testing
run `pytest`

# Notes:

- I'd break up models and views to be its own folder, etc.
- I decided to make make an abstract user for soft delete, [as in](https://docs.djangoproject.com/en/dev/topics/auth/customizing/#extending-the-existing-user-model)
  - Assumption: we will not use `is_active` as a soft delete because the use of it is different. I would ask for clarification in real life.
- I also added the DB 

TODO: ignore db and venv

## Tests:
- With more time I'd like to break up and co-locate the tests, but it asked me to drop the tests in one file so I did 🙏

# Login
SuperUser
SuperPassword
TODO: remove later