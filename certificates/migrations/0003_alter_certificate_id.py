# Generated by Django 4.2.3 on 2023-07-29 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0002_rename_issue_date_certificate_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
