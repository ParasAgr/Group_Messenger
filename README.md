# Group_messenger

Group_messenger is a Python project for sending Group messages

## Installation

please install virtualenv

```bash
>>> pip install virtualenv
>>> python -m virtualenv env
>>> .\env\Scripts\activate

>>> git clone https://github.com/ParasAgr/Group_Messenger.git
>>> cd Group_Messenger  
>>> pip install -r requirment.txt

>>> Create a Database in Postgres
>>> Add Database to the settings.py file 
>>> DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': <db_name>,
        'USER': <user_name>,
        'PASSWORD': <password>,
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
>>> python manage.py makemigrations
>>> python manage.py migrate
>>> python manage.py runserver

```

## Usage
This project has nine end point for your convenience. 


# ADD Messenger User by Admin 
```api
API : http://127.0.0.1:8000/api/add_user/
METHOD: POST
BODY: {
           "username":"rachel",
           "password":"test@123",
           "email":"rache@zane.com",
           "first_name":"rachel",
           "last_name":"zane"
      }
HEADER: {
      Authorization : Token bd2ab48bc3ecd8e3e3b1c86b22aa2fc1e7f89caf           # Superuser Token
      }
RETURN: status
```

# EDIT Messenger User INFO by Admin 
```api
API : http://127.0.0.1:8000/api/edit_user/
METHOD: PUT
BODY: {
      "user_id" : 1,
      <!-- And other fileds which are required to be updated ("username" : value, "first_name" : value, "last_name" : value) -->   
      }
HEADER: {
      Authorization : Token bd2ab48bc3ecd8e3e3b1c86b22aa2fc1e7f89caf          # Superuser Token
      }
RETURN: status
```

# SIGN IN
```api
API : http://127.0.0.1:8000/api/signin/
METHOD: POST
BODY: {
          "username":"rachel",
          "password":"test@123"
      }
return: token
```

# SEND MESSAGE
```api
API : http://127.0.0.1:8000/api/send_message/
METHOD: POST
BODY: {
    "group": 1,
    "message" : "Hii There"
}
HEADER: {
         Authorization : Token 7c9b155a86775f44030a03b939de4c6e6f1ff3b5             #Registered User Token
        }

return: status
```

# LIKE MESSAGE
```api
API : http://127.0.0.1:8000/api/like_message/
METHOD: POST
BODY: {
    "id" : 1           #Every Message will have unique id
      }
HEADER: {
         Authorization : Token 7c9b155a86775f44030a03b939de4c6e6f1ff3b5             #Registered User Token
        }

return: status
```

# CREATE GROUP
```api
API http://127.0.0.1:8000/api/create_group/
MOETHOD: POST
BODY : {
      "group_name": "demo group"
      }
HEADER: {
         Authorization : Token 7c9b155a86775f44030a03b939de4c6e6f1ff3b5             #Registered User Token
        }

return: status
```

# DELETE GROUP 
```api
API http://127.0.0.1:8000/api/delete_group/
MOETHOD: DELETE
BODY : {
      "group_id" : 1
      }
HEADER : {
         Authorization : Token 7c9b155a86775f44030a03b939de4c6e6f1ff3b5             #Registered User Token
        }

return: status
```

# ADD MEMBER TO THE GROUP
```api
API http://127.0.0.1:8000/api/add_member/
MOETHOD: PATCH
BODY : {
    "group_id": 1,
    "new_member": 3   [>>>>>>>>>>>>> user_id is given here(it will add the user to the group only if the user is already present and registered otherwise it will not add)]
      }
HEADER: {
         Authorization : Token 7c9b155a86775f44030a03b939de4c6e6f1ff3b5                  #Registered User Token
        }

return: status
```
