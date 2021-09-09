from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def validador_basico(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        SOLO_LETRAS = re.compile(r'^[a-zA-Z.áéíóúÁÉÍÓÚ ]+$')

        errors = {}

        if len(postData['first_name']) < 2:
            errors['first_name_len'] = "El nombre debe tener al menos 2 caracteres de largo.";

        if len(postData['last_name']) < 2:
            errors['last_name_len'] = "El apellido debe tener al menos 2 caracteres de largo.";

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "correo invalido. Ingrese correo valido."

        all_users = User.objects.all()
        for user in all_users:
            if postData['email'] == user.email:
                errors['email_repetido'] = "Este correo ya ha sido ocupado."

        if not SOLO_LETRAS.match(postData['first_name']):
            errors['solo_letras'] = "El nombre solo debe contener letras."

        if not SOLO_LETRAS.match(postData['last_name']):
            errors['solo_letras'] = "El apellido solo debe contener letras."

        if len(postData['password']) < 8:
            errors['password'] = "contraseña debe tener al menos 8 caracteres";

        if postData['password'] != postData['password_confirm'] :
            errors['password_confirm'] = "contraseña y confirmar contraseña no son iguales. "

        return errors

    def validador_edit(self, postData, id):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        SOLO_LETRAS = re.compile(r'^[a-zA-Z.áéíóúÁÉÍÓÚ ]+$')

        errors = {}

        if len(postData['first_name']) < 2:
            errors['first_name_len'] = "El nombre debe tener al menos 2 caracteres de largo.";

        if len(postData['last_name']) < 2:
            errors['last_name_len'] = "El apellido debe tener al menos 2 caracteres de largo.";

        if not SOLO_LETRAS.match(postData['first_name']):
            errors['solo_letras'] = "El nombre solo debe contener letras."

        if not SOLO_LETRAS.match(postData['last_name']):
            errors['solo_letras'] = "El apellido solo debe contener letras."

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "correo invalido. Ingrese correo valido."

        all_users = User.objects.all().exclude(id=int(id))
        for user in all_users:
            if postData['email'] == user.email:
                errors['email_repetido'] = "Este correo ya ha sido ocupado por otro usuario."
                break

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=70)

    # megustas
    # citas

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"


class citaManager(models.Manager):
    def validador_basico(self, postData):
        SOLO_LETRAS = re.compile(r'^[a-zA-Z.áéíóúÁÉÍÓÚ ]+$')

        errors = {}

        if len(postData['autor']) < 2:
            errors['autor_len'] = "El nombre del autor debe tener al menos 2 caracteres de largo.";

        if len(postData['contenido']) < 2:
            errors['contenido_len'] = "La cita debe tener al menos 2 caracteres de largo.";

        if not SOLO_LETRAS.match(postData['autor']):
            errors['solo_letras'] = "El nombre del autor solo debe contener letras."

        if not SOLO_LETRAS.match(postData['contenido']):
            errors['solo_letras'] = "La cita solo debe contener letras."

        # FALTA QUE SOLO PUEDE PONER MG UNA VEZ
        #all_users = User.objects.all()
        #for user in all_users:
        #    if postData['email'] == user.email:
        #        errors['email_repetido'] = "Este correo ya ha sido ocupado."

        return errors

class Cita(models.Model):
    autor = models.CharField(max_length=100)
    contenido = models.CharField(max_length=500)
    
    megustas = models.ManyToManyField(User, related_name="megustas")
    num_megustas =  models.IntegerField()

    usuarios = models.ForeignKey(User, related_name="cita", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = citaManager()

    def __str__(self):
        return f"{self.contenido}"

    def __repr__(self):
        return f"{self.autor}"


