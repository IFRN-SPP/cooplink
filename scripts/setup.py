import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

import django

django.setup()

from app.models import UserProfile, Institution

username = "admin@email.com"
password = "senha"
full_name = "Administrador"

# Cria o superusuário e a instituição inicial
a = UserProfile.objects.create_superuser(
    username=username, password=password, first_name=full_name
)
b = Institution.objects.create(name="COOPPOTENGI", cnpj="0000")
b.save()
a.institution = b
a.save()

print(" \nYour super user has been created.")
print(
    f"Login with \n \nusername: {username} \npassword: {password} \n \nATTENTION: Dont lose these credentials."
)
