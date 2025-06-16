from django.contrib import admin

from .models import CustomUser, Premise, Client, Rental

admin.site.register(CustomUser)
admin.site.register(Premise)
admin.site.register(Client)
admin.site.register(Rental)
