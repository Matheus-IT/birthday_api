from django.db import models


class Member(models.Model):
    name = models.CharField(max_length=50)
    profile_picture = models.ImageField()
    phone_number = models.CharField(max_length=12)
    birth_date = models.DateField()


class Auth(models.Model):
    # eis a questão
    pass


class Manager(models.Model):
    member_info = models.ForeignKey(Member, null=True)
    auth = models.ForeignKey(Auth)
