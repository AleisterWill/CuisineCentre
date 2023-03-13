# Generated by Django 4.1.7 on 2023-03-13 05:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_loaimonan_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuahang',
            name='menu_set',
            field=models.ManyToManyField(null=True, related_name='menu_set', to='app.menu'),
        ),
        migrations.AlterField(
            model_name='cuahang',
            name='rating_set',
            field=models.ManyToManyField(null=True, related_name='rating_set', to='app.ratingcuahang'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='monan_set',
            field=models.ManyToManyField(null=True, related_name='monan_set', to='app.monan'),
        ),
        migrations.AlterField(
            model_name='monan',
            name='loaimonan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='app.loaimonan'),
        ),
        migrations.AlterField(
            model_name='monan',
            name='rating_set',
            field=models.ManyToManyField(null=True, related_name='rating_set', to='app.ratingmonan'),
        ),
    ]
