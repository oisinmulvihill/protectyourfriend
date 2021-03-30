from django.contrib import admin

from api.models import PolicyType
from api.models import Breed


admin.site.register(PolicyType)
admin.site.register(Breed)
