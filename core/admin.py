from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import *

class ProfileInline(admin.StackedInline):
    model = UserProfile; can_delete = False
    fields = ('rol','guruhlar','bolim','kafedra')

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username','get_full_name','get_rol','is_staff')
    def get_rol(self, obj):
        try: return obj.profile.get_rol_display()
        except: return '—'
    get_rol.short_description = 'Rol'

admin.site.unregister(User); admin.site.register(User, UserAdmin)

@admin.register(Fakultet)
class FakultetAdmin(admin.ModelAdmin):
    list_display = ('nomi',)
    search_fields = ('nomi',)

@admin.register(Kafedra)
class KafedraAdmin(admin.ModelAdmin):
    list_display = ('nomi','fakultet','mudiri','kerakli_sert')
    list_filter = ('fakultet',)

@admin.register(Bolim)
class BolimAdmin(admin.ModelAdmin):
    list_display = ('nomi','boshlig','kerakli_sert')

@admin.register(Guruh)
class GuruhAdmin(admin.ModelAdmin):
    list_display = ('nomi','fakultet','kurs','tyutor','kerakli_sert')
    list_filter = ('fakultet','kurs')

@admin.register(Talaba)
class TalabaAdmin(admin.ModelAdmin):
    list_display = ('fio','guruh'); search_fields = ('fio',); list_filter = ('guruh__fakultet','guruh')

@admin.register(Xodim)
class XodimAdmin(admin.ModelAdmin):
    list_display = ('fio','bolim','lavozim'); search_fields = ('fio',); list_filter = ('bolim',)

@admin.register(Oqituvchi)
class OqituvchiAdmin(admin.ModelAdmin):
    list_display = ('fio','kafedra','lavozim'); search_fields = ('fio',); list_filter = ('kafedra',)

@admin.register(Sertifikat)
class SertAdmin(admin.ModelAdmin):
    list_display = ('egasi_fio','egasi_tur','nomi','tashkilot','berilgan','yuklagan','yaratilgan')
    list_filter = ('yaratilgan',); search_fields = ('nomi','talaba__fio','xodim__fio','oqituvchi__fio')
    date_hierarchy = 'yaratilgan'; readonly_fields = ('yaratilgan',)
