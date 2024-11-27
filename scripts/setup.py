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
    print("== Initial Setup ==")

    # Superuser input
    username = "admin@email.com"
    password = "senha"
    full_name = "Admin User"

    # Cooperative input
    coop_name = input("Enter the name for the cooperative: ").strip()
    cnpj = input("Enter the CNPJ for the cooperative: ").strip()
    logo_path = input(
        "Enter the relative path to the logo file from 'static/': "
    ).strip()
    extended_name = input("Enter the extended name for the cooperative: ").strip()
    catch_phrase = input("Enter the catch phrase for the cooperative: ").strip()
    location = input("Enter the location for the cooperative (Cidade / UF): ").strip()

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
            location=location
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
