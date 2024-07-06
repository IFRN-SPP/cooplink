# Create Super User and first Institution
from app.models import UserProfile, Institution

username = 'admin'
password = 'senha'
email = 'admin@example.com'

a = UserProfile.objects.create_superuser(username=username, password=password, email=email)
b = Institution.objects.create(name='initial', cnpj='0000')
b.save()
a.institution = b
a.save()

print(' \nYour super user has been created.')
print(f'Login with \n \nusername: {username} \npassword: {password} \n \nATTENTION: Dont lose these credentials.')

exit()