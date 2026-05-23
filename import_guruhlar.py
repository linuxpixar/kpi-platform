"""
Guruhlarni bazaga kiritish skripti.
Ishlatish: python3 import_guruhlar.py
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sertifikat_platform.settings')
django.setup()

from core.models import Fakultet, Guruh

guruhlar = [
    "CHIN-AU-23","ENG-AU-22","ENG-AU-23","ENG-AU-24","ENG-AU-25",
    "ENG-BU-22","ENG-BU-23","ENG-BU-24","ENG-BU-25",
    "ENG-CR-23","ENG-CR-25","ENG-CU-22","ENG-CU-24",
    "ENG-DU-23","ENG-DU-24","ENG-DU-25",
    "ENG-EU-23","ENG-EU-24","ENG-EU-25",
    "ENG-FU-23","ENG-FU-24","ENG-FU-25",
    "ENG-GU-23","ENG-GU-24","ENG-HR-23",
    "FAR-AU-23","FRA-AU-22","FRA-AU-23","FRA-AU-24",
    "GER-AU-22","GER-AU-23","GER-AU-24","GER-AU-25",
    "GID-AU-22","GID-AU-23","JAP-AU-23",
    "K.ENG-AU-23","K.ENG-AU-24","K.ENG-AU-25",
    "K.ENG-BU-23","K.ENG-BU-24","K.ENG-BU-25",
    "KLA-AU-23","KLA-AU-24","KLA-AU-25",
    "K.MBX-AU-23","KOR-AU-23","KOR-AU-24","KOR-AU-25",
    "K.RUA-AR-23","K.RUA-AR-24","K.RUA-AR-25",
    "K.RUS-AR-23","K.RUS-AR-24","K.RUS-AR-25","K.RUS-BR-23",
    "K.XTA-AU-23","K.XTA-AU-24","K.XTA-AU-25",
    "K.XTA-BU-23","K.XTA-BU-24","K.XTA-BU-25",
    "M.ADA-AU-24","M.ADA-AU-25",
    "MBX-AU-22","MBX-AU-23","MBX-BU-22","MBX-BU-23",
    "M.L.ENG-AU-24","M.LNF-AU-24","M.LNG-AU-24",
    "M.LNGE-AU-25","M.LNGK-AU-25","M.LNGN-AU-25",
    "M.QTTL-AU-24","M.QTTL-AU-25",
    "M.RUS-AU-24","M.RUS-AU-25",
    "M.XTA-AU-24","M.XTA-AU-25","PER-AU-23",
    "RUA-AR-22","RUA-AR-23","RUA-AR-24","RUA-AR-25",
    "RUA-BR-22","RUA-BR-23","RUA-BR-24","RUA-BR-25",
    "RUA-CR-25","RUA-DR-25",
    "RUS-AR-22","RUS-AR-23","RUS-AR-24","RUS-AR-25",
    "RUS-BR-23","RUS-BR-24","RUS-BR-25",
    "RUS-CR-23","RUS-DR-23",
    "TM-AU-24","TM-AU-25","TM-BU-24",
    "TNA-AU-22","TNA-AU-23","TNA-AU-24","TNA-AU-25","TNG-AU-23",
    "XTA-AU-22","XTA-AU-23","XTA-AU-24","XTA-AU-25",
    "XTA-BU-22","XTA-BU-23","XTA-BU-24","XTA-BU-25",
    "XTA-CR-25","XTA-CU-22","XTA-CU-23","XTA-CU-24",
    "XTA-DU-22","XTA-DU-23","XTA-DU-24","XTA-DU-25",
    "XTA-EU-23","XTA-EU-24","XTA-EU-25",
    "XTA-FU-23","XTA-FU-24","XTA-FU-25",
    "XTA-GU-23","XTA-GU-24","XTA-GU-25",
    "XTA-HU-23","XTA-HU-24","XTA-HU-25",
    "XTA-IU-23","XTA-IU-24","XTA-IU-25",
    "XTA-JU-23","XTA-JU-24","XTA-JU-25",
    "XTA-KU-24","XTA-KU-25",
]

kurs_map = {'22': 4, '23': 3, '24': 2, '25': 1}

# Fakultet yaratish
fakultet, _ = Fakultet.objects.get_or_create(nomi='Chet tillar')

yangi = 0
mavjud = 0
for g in guruhlar:
    yil = g.split('-')[-1]
    kurs = kurs_map.get(yil, 1)
    obj, created = Guruh.objects.get_or_create(
        nomi=g,
        defaults={'fakultet': fakultet, 'kurs': kurs, 'kerakli_sert': 1}
    )
    if created:
        yangi += 1
    else:
        mavjud += 1

print(f"\n✅ Tayyor!")
print(f"   Yangi qo'shildi : {yangi} ta")
print(f"   Allaqachon bor  : {mavjud} ta")
print(f"   Jami guruh      : {Guruh.objects.count()} ta")
