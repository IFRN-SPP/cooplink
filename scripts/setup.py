import os
import sys

# Set up the Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

import django

django.setup()

from app.models import Cooperative, UserProfile, Institution
from django.conf import settings


def main():
    # Collect static
    from django.core.management import call_command

    call_command("collectstatic", verbosity=0, interactive=False)

    print("== Initial Setup ==")

    # Superuser input
    username = "admin@email.com"
    password = "senha"
    full_name = "Admin User"

    # Cooperative input
    coop_name = (
        input(
            "Enter the name for the cooperative (Press Enter for default: 'Cooperativa'): "
        ).strip()
        or "Cooperativa"
    )

    cnpj = (
        input(
            "Enter the CNPJ for the cooperative (Press Enter for default: '123.456.789-00'): "
        ).strip()
        or "123.456.789-00"
    )

    logo_path = (
        input(
            "Enter the relative path to the logo file from 'static/' (Press Enter for default): "
        ).strip()
        or "assets/logo.png"
    )
    extended_name = (
        input(
            "Enter the extended name for the cooperative (Press Enter for default): "
        ).strip()
        or "Cooperativa Com Um Nome Extensivamente Longo"
    )

    catch_phrase = (
        input(
            "Enter the catch phrase for the cooperative (Press Enter for default): "
        ).strip()
        or "Um lema muito legal e interessante"
    )

    location = (
        input(
            "Enter the location for the cooperative 'Cidade / UF' (Press Enter for default): "
        ).strip()
        or "Cidade / BR"
    )

    try:
        # Validate the logo path
        if logo_path:
            static_logo_path = os.path.join(settings.STATIC_ROOT, logo_path)
            if not os.path.isfile(static_logo_path):
                print(f"Error: The file '{static_logo_path}' does not exist.")
                return

        # Create or update the cooperative
        cooperative, created_coop = Cooperative.objects.update_or_create(
            defaults={"logo": logo_path},
            name=coop_name,
            extended_name=extended_name,
            catch_phrase=catch_phrase,
            location=location,
        )
        if created_coop:
            print(f"Cooperative '{coop_name}' created successfully.")
        else:
            print(f"Cooperative '{coop_name}' already existed and was updated.")

        # Create the institution
        institution, created_inst = Institution.objects.get_or_create(
            name=coop_name, cnpj=cnpj
        )
        if created_inst:
            print(f"Institution '{coop_name}' created successfully.")
        else:
            print(f"Institution '{coop_name}' already existed.")

        # Create the superuser
        superuser = UserProfile.objects.create_superuser(
            username=username, password=password, first_name=full_name
        )
        superuser.institution = institution
        superuser.save()
        print("\nSuperuser created successfully:")
        print(f"Email: {username}")
        print(f"Password: {password}")

    except Exception as e:
        print(f"Error setting up the system: {e}")


if __name__ == "__main__":
    main()
