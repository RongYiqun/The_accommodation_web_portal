We have launched our website and database in online servers, you can access it via http://psychecraft.com.

You can also run and configure it on the localhost, in that case you need to configure your environment and dependencies.
You can use the following commands to install all modules:
Pip install Django
Pip install django-crispy-forms
Pip install psycopg2
Pip install geocoder
Pip install Pillow

Once all modules are installed, you can open the command line on the project directory,
and type the following command:


reminder:
if you want to run this project,
The file setting.py under the project folder must be completed, by replace XXX by your database information.
see more information in https://docs.djangoproject.com/en/2.0/ref/settings/#databases . 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'XXX',
        'USER': 'XXX',
        'PASSWORD': 'XXX',
        'HOST': 'XXX',
        'PORT': 'XXX',
    }
}


Python manage.py runserver 8080

If everything is ok, the server is already start, copy the link http://127.0.0.1:8080/ to your browser then you can access the website.


creator:
  1. HengmingWang(ScrumMaster/Developer)z5137595 email: z5137595@ad.unsw.edu.au
  2. Zhihao Ye (Developer) z5129023 email: z5129023@ad.unsw.edu.au
  3. YiqunRong (Developer)z5150126 email: z5150126@ad.unsw.edu.au
