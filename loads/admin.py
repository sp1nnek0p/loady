from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Load)
admin.site.register(Tag)
admin.site.register(DetailUser)
admin.site.register(LoadMessage)
admin.site.register(DirectMessage)
admin.site.register(Vehicle)

