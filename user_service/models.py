from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
# from django.contrib.auth.models import UserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, cpf, password, birth_date, status_user, first_name, last_name, card):
        user = self.model(
            email=self.normalize_email(email)
        )
        user.cpf = cpf
        user.birth_date = birth_date
        user.status_user = status_user
        user.first_name = first_name
        user.last_name = last_name
        user.card = card
        user.set_password(password)
        user.is_staff = False
        user.is_active = True
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, cpf, password, birth_date, status_user, first_name, last_name):
        user = self.model(
            email=self.normalize_email(email)
        )
        user.cpf = cpf
        user.birth_date = birth_date
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.status_user = status_user
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email):
        return self.get(email=email)


class Profile(AbstractBaseUser, PermissionsMixin):

    cpf = models.CharField(unique=True, max_length=11)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    status_user = models.BooleanField(default=True, verbose_name='status') # soft delete here
    birth_date = models.DateField(verbose_name='data de nascimento', blank=True, null=True)
    is_staff = models.BooleanField(default=False, verbose_name='administrador')
    is_superuser = models.BooleanField(default=False, verbose_name='superusuario')
    date_joined = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to="user_images", max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['cpf']

    objects = CustomUserManager()

    class Meta:
        verbose_name = u'Profile'
        verbose_name_plural = u'Profiles'

    def get_short_name(self):
        return self.email

    def natural_key(self):
        return self.email

    def __str__(self):
        return self.email


class Card(models.Model):
    number = models.CharField(unique=True, max_length=16, blank=False, verbose_name='número')
    cvv = models.CharField(blank=False, null=False, max_length=3, verbose_name='codigo de segurança')
    validation = models.DateField(verbose_name='Validade')
    holder_name = models.CharField(max_length=30, blank=False, verbose_name='Nome do proprietário')
    cpf_cnpj = models.CharField(max_length=20, blank=False, verbose_name='Cpf/Cnpj do proprietário')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['profile']

    class Meta:
        verbose_name = u'Card'
        verbose_name_plural = u'Cards'

    def __str__(self):
        return self.number
