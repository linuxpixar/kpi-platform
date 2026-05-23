import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sertifikat_platform.settings')
django.setup()

from core.models import Kafedra, Bolim, Xodim, Oqituvchi

x = Xodim.objects.count()
o = Oqituvchi.objects.count()
k = Kafedra.objects.count()
b = Bolim.objects.count()

Xodim.objects.all().delete()
Oqituvchi.objects.all().delete()
Kafedra.objects.all().delete()
Bolim.objects.all().delete()

print(f"✅ O'chirildi:")
print(f"   Xodimlar     : {x} ta")
print(f"   O'qituvchilar: {o} ta")
print(f"   Kafedralar   : {k} ta")
print(f"   Bo'limlar    : {b} ta")
