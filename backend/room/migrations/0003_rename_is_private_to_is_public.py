from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0002_room_username_nullable'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='is_private',
            new_name='is_public',
        ),
        migrations.AlterField(
            model_name='room',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]
