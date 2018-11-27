# Generated by Django 2.0.5 on 2018-10-02 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_auto_20180912_1409'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='host',
            name='listings_count',
        ),
        migrations.AddField(
            model_name='host',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='host',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Unknown')], default='U', max_length=1),
        ),
        migrations.AddField(
            model_name='host',
            name='good_credit',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='host',
            name='verifications',
            field=models.TextField(blank=True, null=True),
        ),
    ]