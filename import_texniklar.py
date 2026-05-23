import os, sys, django, re
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sertifikat_platform.settings')
django.setup()

from core.models import Bolim, Xodim

# Fayldan texnik xodimlarni o'qish
with open('report.xls', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

all_tds = re.findall(r'<td[^>]*>(.*?)</td>', content, re.DOTALL)
clean_tds = [re.sub(r'<[^>]+>','',t).replace('&amp;','&').strip() for t in all_tds]

start = 0
for i, td in enumerate(clean_tds):
    if td == 'No.':
        start = i + 20
        break

COLS = 20
data = []
i = start
while i + COLS <= len(clean_tds):
    row = clean_tds[i:i+COLS]
    if row[0].isdigit():
        data.append(row)
        i += COLS
    else:
        i += 1

# Texnik xodimlar
texniklar_raw = [r for r in data if 'Texnik' in r[3]]

# FIO tozalash
def tozala(fio):
    return fio.replace("''''","'").replace("''","'").strip()

# Bo'lim
bolim, _ = Bolim.objects.get_or_create(
    nomi='Texnik xodimlar',
    defaults={'kerakli_sert': 1}
)

yangi = 0
mavjud = 0
for r in texniklar_raw:
    fio = tozala(r[2])
    if not fio or len(fio) < 3:
        continue
    if not Xodim.objects.filter(fio=fio, bolim=bolim).exists():
        Xodim.objects.create(fio=fio, bolim=bolim, lavozim='')
        yangi += 1
        print(f"  ✅ {fio}")
    else:
        mavjud += 1

print(f"\n{'='*50}")
print(f"✅ TAYYOR!")
print(f"  Yangi qo'shildi : {yangi} ta")
print(f"  Allaqachon bor  : {mavjud} ta")
print(f"  Jami texnik     : {Xodim.objects.filter(bolim=bolim).count()} ta")
