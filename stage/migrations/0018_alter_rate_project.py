# Generated by Django 3.2.7 on 2021-09-19 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stage', '0017_auto_20210919_0847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stage.project'),
        ),
    ]