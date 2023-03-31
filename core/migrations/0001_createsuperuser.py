import os

from django.db import migrations
from django.db.backends.postgresql.schema import DatabaseSchemaEditor
from django.db.migrations.state import StateApps

import google.auth
from google.cloud import secretmanager

from authentication.models import CustomUser


def createsuperuser(apps: StateApps, schema_editor: DatabaseSchemaEditor) -> None:
    """
    Dynamically create an admin user as part of a migration
    Password is pulled from Secret Manger (previously created as part of tutorial)
    """
    if os.environ.get("ADMIN_PASSWORD", None):
        admin_password = os.environ.get("ADMIN_PASSWORD")
    else:
        admin_password = "test"

    # Create a new user using acquired password, stripping any accidentally stored newline characters
    CustomUser.objects.create_superuser(
        "11755088450", "+5581991157486", "Gabriel", password=admin_password.strip()
    )


class Migration(migrations.Migration):

    initial = True
    dependencies = []
    operations = [migrations.RunPython(createsuperuser)]
