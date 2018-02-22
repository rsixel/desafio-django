from django.contrib import admin
from .models import Enquete, Resposta

# admin.site.register(Enquete)


class RespostaInline(admin.StackedInline):
    model = Resposta
    extra = 3


class EnqueteAdmin(admin.ModelAdmin):
    inlines = [
        RespostaInline
    ]

admin.site.register(Enquete, EnqueteAdmin)
