from django.contrib import admin

# Register your models here.
from .models import StudentDB,Notifications,Appliedproject
# Register your models here.
admin.site.register(StudentDB)
admin.site.register(Notifications)
admin.site.register(Appliedproject)
