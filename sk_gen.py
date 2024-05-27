from django.core.management.utils import get_random_secret_key

print("This is your SECRET_KEY")
print("")
print(get_random_secret_key())
print("")
print("SECURITY WARNING: keep the secret key used in production secret!")