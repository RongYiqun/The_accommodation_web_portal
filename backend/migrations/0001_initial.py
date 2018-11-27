# Generated by Django 2.1 on 2018-08-23 06:35

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Myuser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('verification', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Bookings',
            fields=[
                ('booking_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('listing_id', models.BigIntegerField()),
                ('visitor_id', models.BigIntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('cancellation', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing_id', models.BigIntegerField()),
                ('calendar_date', models.DateField(blank=True, null=True)),
                ('available', models.BooleanField()),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.TextField(blank=True, null=True)),
                ('summary', models.TextField(blank=True, null=True)),
                ('space', models.TextField(blank=True, null=True)),
                ('neighbourhood_overview', models.TextField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('transit', models.TextField(blank=True, null=True)),
                ('picture_url', models.URLField(blank=True, null=True)),
                ('host_id', models.BigIntegerField()),
                ('host_name', models.TextField(blank=True, null=True)),
                ('host_since', models.DateField(blank=True, null=True)),
                ('host_location', models.TextField(blank=True, null=True)),
                ('host_about', models.TextField(blank=True, null=True)),
                ('host_picture_url', models.URLField(blank=True, null=True)),
                ('host_total_listings_count', models.IntegerField(blank=True, null=True)),
                ('host_verifications', models.TextField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=200, null=True)),
                ('state', models.CharField(blank=True, max_length=200, null=True)),
                ('zipcode', models.IntegerField(blank=True, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('property_type', models.CharField(blank=True, max_length=200, null=True)),
                ('room_type', models.CharField(blank=True, max_length=200, null=True)),
                ('accommodates', models.IntegerField(blank=True, null=True)),
                ('bathrooms', models.FloatField(blank=True, null=True)),
                ('bedrooms', models.IntegerField(blank=True, null=True)),
                ('bed', models.IntegerField(blank=True, null=True)),
                ('bed_type', models.CharField(blank=True, max_length=200, null=True)),
                ('amenities', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('cleaning_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('minimum_nights', models.IntegerField(blank=True, null=True)),
                ('number_of_reviews', models.IntegerField(blank=True, null=True)),
                ('review_scores_rating', models.IntegerField(blank=True, null=True)),
                ('cancellation_policy', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('listing_id', models.BigIntegerField()),
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('reviews_date', models.DateField(blank=True, null=True)),
                ('reviewer_id', models.BigIntegerField()),
                ('reviewer_name', models.CharField(blank=True, max_length=200, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('myuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('picture', models.URLField(blank=True, null=True)),
                ('since', models.DateField(blank=True, null=True)),
                ('listings_count', models.IntegerField(blank=True, null=True)),
                ('about', models.TextField(blank=True, null=True)),
                ('location', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('backend.myuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('myuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Unknown')], default='U', max_length=1)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('portrait', models.ImageField(blank=True, null=True, upload_to='')),
                ('good_credit', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('backend.myuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='myuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]