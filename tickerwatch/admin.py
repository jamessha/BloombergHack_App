from django.contrib import admin
from tickerwatch.models import Stock, UserProfile

# Register your models here.
admin.site.register(Stock)
admin.site.register(UserProfile)
