## Django-OAuth2-App
A basic application in Django using OAuth2.0 for Authentication.

### Prerequisites
- Python 3.2+ 
- Django 3.0+
- django-oauth-toolkit (uses python 3.2+)
- Django Rest Framework 3.0+
> You can tune your venv accordingly.

### Installation Steps
- Clone the repo

` git clone https://github.com/Arnesh07/Django-Auth-App `
- Make a private_constants.py file in the users directory
- Add `CLIENT_ID = ''` and `CLIENT_SECRET = ''` to it. These are to be updated later.
- Make migrations (Make sure you are in the project's root)

` python manage.py makemigrations users`

` python manage.py migrate`
- Run the server

`python manage.py runserver`

**To be able to login, there should be atleast one registered application.**

- To register an application, first create a superuser.
`python manage.py createsuperuser`
- Enter the email and password to successfully create a superuser.
- Then run the server and login to the admin portal using that superuser.
- Redirect to `o/applications` endpoint.
- Create an application.
- Update the client id and the client secret in the private_constants.py file.

### Overview
#### 1. **models.py**: 
User class uses subclasses AbstractBaseUser and PermissionsMixin, which allows
us to modify the model's fields accordingly.
email, name and password fields are specified.
is_staff and is_superuser fields are required for the determination of admin.
groups and permissions are enabled by the PermissionsMixin Class. 

**username is not used.**

`USERNAME_FIELD = 'email'` is used to shift the control of authentication to email
from username.

UserManager uses the subclass BaseUserManager.

`create_user` and `create_superuser` methods are overriden to make use of the
customized fields. 

#### 2. **views.py**
- SignupView:
It takes use of the generic CreateAPIView of the DRF and uses the UserSerializer to
create user objects.
- LoginView:
This uses the APIView and overrides the POST request to call the `o/token/` endpoint
to retrieve the token after authentication. A better alternative would have been to not call the `o/token/` endpoint and instead manually imported the required code and call the functions directly.
- HomePageView:
This is based on the endpoint `/home/`. If the user is authorized, this simply returns a simple HttpResponse.

#### 3. **serializers.py**
The `UserSerializer` uses the predefined ModelSerializer to simplify the code.
It also overrides the create method and makes use of `make_password` to ensure that
the passwords are hashed and stored in the database. It makes use of the default
PBKDF2 algorithm.

#### 4. **tests.py**
It contains unit tests for the UserManagerClass and all the Views.
