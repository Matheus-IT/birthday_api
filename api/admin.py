from django.contrib import admin
from api.models import Auth, Manager, Member

admin.site.register([Auth, Manager, Member])
