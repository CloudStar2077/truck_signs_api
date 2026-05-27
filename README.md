<div align="center">

![Truck Signs](./screenshots/Truck_Signs_logo.png)

# Signs for Trucks

![Python version](https://img.shields.io/badge/Pythn-3.8.10-4c566a?logo=python&&longCache=true&logoColor=white&colorB=pink&style=flat-square&colorA=4c566a) ![Django version](https://img.shields.io/badge/Django-2.2.8-4c566a?logo=django&&longCache=truelogoColor=white&colorB=pink&style=flat-square&colorA=4c566a) ![Django-RestFramework](https://img.shields.io/badge/Django_Rest_Framework-3.12.4-red.svg?longCache=true&style=flat-square&logo=django&logoColor=white&colorA=4c566a&colorB=pink)


</div>


# Truck Signs API 

This project provides a Dockerized Django REST API for managing truck sign products, categories, and orders with PostgreSQL as the database backend.
Gunicorn and Nginx are used to ruDescription
n the application in production. Nginx handles reverse proxying and static content delivery, while Gunicorn serves the Python web application as a WSGI application server.
The setup is managed entirely through manual Docker commands without Docker Compose.

## Table of Contents
* [Description](#Description)
* [Quickstart](#Quickstart)
* [Usage](#Usage)

## Description

__Signs for Trucks__ is an online store to buy pre-designed vinyls with custom lines of letters (often call truck letterings). The store also allows clients to upload their own designs and to customize them on the website as well. Aside from the vinyls that are the main product of the store, clients can also purchase simple lettering vinyls with no truck logo, a fire extinguisher vinyl, and/or a vinyl with only the truck unit number (or another number selected by the client).

### Settings

The __settings__ folder inside the trucks_signs_designs folder contains the different setting's configuration for each environment (so far the environments are development, docker testing, and production). Those files are extensions of the base.py file which contains the basic configuration shared among the different environments (for example, the value of the template directory location). In addition, the .env file inside this folder has the environment variables that are mostly sensitive information and should always be configured before use. By default, the environment in use is the decker testing. To change between environments modify the \_\_init.py\_\_ file.

### Models

Most of the models do what can be inferred from their name. The following dots are notes about some of the models to make clearer their propose:
- __Category Model:__ The category of the vinyls in the store. It contains the title of the category as well as the basic properties shared among products that belong to a same category. For example, _Truck Logo_ is a category for all vinyls that has a logo of a truck plus some lines of letterings (note that the vinyls are instances of the model _Product_). Another category is _Fire Extinguisher_, that is for all vinyls that has a logo of a fire extinguisher. 
- __Lettering Item Category:__ This is the category of the lettering, for example: _Company Name_, _VIM NUMBER_, ... Each has a different pricing.
- __Lettering Item Variations:__ This contains a foreign key to the __Lettering Item Category__ and the text added by the client.
- __Product Variation:__ This model has the original product as a foreign key, plus the lettering lines (instances of the __Lettering Item Variations__ model) added by the client.
- __Order:__ Contains the cart (in this case the cart is just a vinyl as only one product can be purchased each time). It also contains the contact and shipping information of the client.
- __Payment:__ It has the payment information such as the time of the purchase and the client id in Stripe.

To manage the payments, the payment gateway in use is [Stripe](https://stripe.com/).

> [!NOTE]  
> Because this repo is for documentation and testing purpose the payments part is missing.

### Brief Explanation of the Views

Most of the views are CBV imported from _rest_framework.generics_, and they allow the backend api to do the basic CRUD operations expected, and so they inherit from the _ListAPIView_, _CreateAPIView_, _RetrieveAPIView_, ..., and so on.

The behavior of some of the views had to be modified to address functionalities such as creation of order and payment, as in this case, for example, both functionalities are implemented in the same view, and so a _GenericAPIView_ was the view from which it inherits. Another example of this is the _UploadCustomerImage_ View that takes the vinyl template uploaded by the clients and creates a new product based on it.


## Quickstart

Prerequisites
- Docker (version 20.10 or higher) installed
- Git installed



Clone Repository 
```bash
git clone git@github.com:CloudStar2077/truck_signs_api.git &&
cd truck_signs_api
```

How to build the Image 

Build the Docker image:
```bash
docker build -t truck_signs_api .
```

Copy the example environment file and fill in your values:
```bash
cp example.env .env   
```

Run the Containers

Create the shared network and the volumes:
```bash
docker network create django_net &&
docker volume create postgres_data &&
docker volume create django_static &&
docker volume create django_media
```

Start the PostgreSQL container:

```bash
docker run -d \
  --name db \
  --network django_net \
  --restart on-failure \
  --env-file .env \
  -v postgres_data:/var/lib/postgresql/data \
  postgres:14-alpine
```

Start the Django container:

```bash
docker run -d \
  --name django_web \
  --network django_net \
  --restart on-failure \
  --env-file .env \
  -v django_static:/app/static \
  -v django_media:/app/media \
  truck_signs_api
```
Start the Nginx container:

```bash
docker run -d \
  --name nginx \
  --network django_net \
  --restart on-failure \
  -p 8020:8020 \
  -v $(pwd)/nginx.conf:/etc/nginx/conf.d/default.conf \
  -v django_static:/app/static \
  -v django_media:/app/media \
  nginx:alpine
```

The API is now available at:

```
http://<YOUR_IP>:8020/truck-signs/products/
```

The Admin Panel is available at:

```
http://<YOUR_IP>:8020/admin
```


## Usage

All configuration is done via a `.env` file. The `Dockerfile` uses python:3.8-slim as the base image and installs all dependencies from `requirements.txt`. The `nginx.conf` is located in the project root and is mounted into the Nginx container as a bind mount. The shell script `entrypoint.sh` is executed inside the container when the container starts.The `.gitignore` defines files and folders that should not be versioned by Git. This excludes temporary files, sensitive data or automatically generated content from the repository. The `.dockerignore` determines which files are not included in the build context when building a Docker image. This excludes unnecessary files and makes Docker builds faster and images smaller.

Clone the repo:
  ```bash
    git clone git@github.com:CloudStar2077/truck_signs_api.git
  ```

Configure the environment variables.
Copy the content of the `example.env` file into a `.env` file:
```bash
cd truck_signs_api
cp example.env .env
```
Then fill in your values:

| Variable | Example Value | Description |
|---|---|---|
| `DOCKER_SECRET_KEY` | `g9!Qv4...` | Django secret key for cryptographic signing |
| `DOCKER_DB_NAME` | `djangodb` | Name of the PostgreSQL database |
| `DOCKER_DB_USER` | `djangouser` | PostgreSQL user |
| `DOCKER_DB_PASSWORD` | `Your_Secure_Password!` | PostgreSQL password |
| `DOCKER_DB_HOST` | `db` | Hostname of the DB container |
| `DOCKER_DB_PORT` | `5432` | PostgreSQL port |
| `POSTGRES_DB` | `djangodb` | Required by the PostgreSQL image (must match `DOCKER_DB_NAME`) |
| `POSTGRES_USER` | `djangouser` | Required by the PostgreSQL image (must match `DOCKER_DB_USER`) |
| `POSTGRES_PASSWORD` | `Your_Secure_Password!` | Required by the PostgreSQL image (must match `DOCKER_DB_PASSWORD`) |
| `DOCKER_EMAIL_HOST_USER` | `you@gmail.com` | E-mail address for sending emails |
| `DOCKER_EMAIL_HOST_PASSWORD` | `your-app-password` | E-mail app password |
| `DJANGO_SUPERUSER_USERNAME` | `admin` | Username for the auto-created superuser |
| `DJANGO_SUPERUSER_EMAIL` | `admin@example.com` | Email for the auto-created superuser |
| `DJANGO_SUPERUSER_PASSWORD` | `Your_Secure_Password!` | Password for the auto-created superuser |

To generate a secure Django Secret Key use
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```
> [!IMPORTANT]  
> Never commit your `.env` file to version control. Make sure `.env` is listed in `.gitignore`.

Build the image from the project root (where the `Dockerfile` is stored):

```bash
docker build -t truck_signs_api .
```

Create network and volumes
```bash
docker network create django_net &&
docker volume create postgres_data &&
docker volume create django_static &&
docker volume create django_media &&
```

Start PostgreSQL:
```bash
docker run -d \
  --name db \
  --network django_net \
  --restart on-failure \
  --env-file .env \
  -v postgres_data:/var/lib/postgresql/data \
  postgres:14-alpine
```

Start Django:
```bash
docker run -d \
  --name django_web \
  --network django_net \
  --restart on-failure \
  --env-file .env \
  -v django_static:/app/static \
  -v django_media:/app/media \
  truck_signs_api
```
Start Nginx:
```bash
docker run -d \
  --name nginx \
  --network django_net \
  --restart on-failure \
  -p 8020:8020 \
  -v $(pwd)/nginx.conf:/etc/nginx/conf.d/default.conf \
  -v django_static:/app/static \
  -v django_media:/app/media \
  nginx:alpine
```
To verify everything is all right check the Logs
```bash
docker logs -f django_web
docker logs -f nginx
docker logs -f db
```

The API is now available at:

```
http://<YOUR_IP>:8020/truck-signs/products/
```

The Admin Panel is available at:

```
http://<YOUR_IP>:8020/admin
```


__NOTE:__ To create Truck vinyls with Truck logos in them, first create the __Category__ Truck Sign, and then the __Product__ (can have any name). This is to make sure the frontend retrieves the Truck vinyls for display in the Product Grid as it only fetches the products of the category Truck Sign.

---

<a name="screenshots"></a>

## Screenshots of the Django Backend Admin Panel

### Mobile View

<div align="center">

![alt text](./screenshots/Admin_Panel_View_Mobile.png)  ![alt text](./screenshots/Admin_Panel_View_Mobile_2.png) ![alt text](./screenshots/Admin_Panel_View_Mobile_3.png)

</div>
---

### Desktop View

![alt text](./screenshots/Admin_Panel_View.png)

---

![alt text](./screenshots/Admin_Panel_View_2.png)

---

![alt text](./screenshots/Admin_Panel_View_3.png)



<a name="useful_links"></a>
## Useful Links

### Postgresql Database
- Setup Database: [Digital Ocean Link for Django Deployment on VPS](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04)

### Docker
- [Docker Oficial Documentation](https://docs.docker.com/)
- Dockerizing Django, PostgreSQL, guinicorn, and Nginx:
    - Github repo of sunilale0: [Link](https://github.com/sunilale0/django-postgresql-gunicorn-nginx-dockerized/blob/master/README.md#nginx)
    - Michael Herman article on testdriven.io: [Link](https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/)

### Django and DRF
- [Django Official Documentation](https://docs.djangoproject.com/en/4.0/)
- Generate a new secret key: [Stackoverflow Link](https://stackoverflow.com/questions/41298963/is-there-a-function-for-generating-settings-secret-key-in-django)
- Modify the Django Admin:
    - Small modifications (add searching, columns, ...): [Link](https://realpython.com/customize-django-admin-python/)
    - Modify Templates and css: [Link from Medium](https://medium.com/@brianmayrose/django-step-9-180d04a4152c)
- [Django Rest Framework Official Documentation](https://www.django-rest-framework.org/)
- More about Nested Serializers: [Stackoverflow Link](https://stackoverflow.com/questions/51182823/django-rest-framework-nested-serializers)
- More about GenericViews: [Testdriver.io Link](https://testdriven.io/blog/drf-views-part-2/)

### Miscellaneous
- Create Virual Environment with Virtualenv and Virtualenvwrapper: [Link](https://docs.python-guide.org/dev/virtualenvs/)
- [Configure CORS](https://www.stackhawk.com/blog/django-cors-guide/)
- [Setup Django with Cloudinary](https://cloudinary.com/documentation/django_integration)



