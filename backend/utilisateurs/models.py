from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = [
        ('admin', 'Administrateur'),
        ('avocat', 'Avocat'),
        ('assistante', 'Assistante'),
    ]

    role = models.CharField(max_length=20, choices=ROLES, default='assistante')
    telephone = models.CharField(max_length=20, blank=True)
    barreau = models.CharField(max_length=100, blank=True)

    # 🔥 AJOUT IMPORTANT
    avocat = models.ForeignKey(
    'self',
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    related_name='assistantes'
)

    def is_avocat(self):
        return self.role == 'avocat'

    def is_assistante(self):
        return self.role == 'assistante'

    def is_admin_cabinet(self):
        return self.role == 'admin'

    def __str__(self):
        return self.get_full_name() or self.username