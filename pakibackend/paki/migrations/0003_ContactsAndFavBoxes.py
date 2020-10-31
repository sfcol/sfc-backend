# Generated by Django 2.2.5 on 2020-10-31 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paki', '0002_HandoverTransaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contactId', models.UUIDField()),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('pictureLink', models.CharField(max_length=1023)),
            ],
            options={
                'db_table': 'paki_backend_contacts',
            },
        ),
        migrations.CreateModel(
            name='FavBoxes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boxId', models.UUIDField()),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paki.Contacts')),
            ],
            options={
                'db_table': 'paki_backend_favoriteboxes',
            },
        ),
        migrations.AddConstraint(
            model_name='contacts',
            constraint=models.UniqueConstraint(fields=('email',), name='unique email contacts'),
        ),
        migrations.AddConstraint(
            model_name='favboxes',
            constraint=models.UniqueConstraint(fields=('boxId', 'contact'), name='unique email contact combination'),
        ),
    ]
