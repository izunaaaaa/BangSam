from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_remove_user_is_realtor"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="phone_number",
            field=models.CharField(max_length=13),
        ),
    ]
