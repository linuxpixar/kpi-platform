"""
Tyutorlarni bazaga kiritish va guruhlarga biriktirish skripti.
Fayl: NamDCHTI_Talabalarni_tyutorlarga_biriktirilishi_06_04_2026.xlsx

Ishlatish: python3 import_tyutorlar.py
"""
import os, sys, django, re
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sertifikat_platform.settings')
django.setup()

from openpyxl import load_workbook
from django.contrib.auth.models import User
from core.models import Guruh, UserProfile

FAYL = os.path.join(os.path.dirname(__file__),
    'NamDCHTI_Talabalarni_tyutorlarga_biriktirilishi_06_04_2026.xlsx')

if not os.path.exists(FAYL):
    print(f"❌ Fayl topilmadi: {FAYL}")
    sys.exit(1)

# ── EXCEL DAN TYUTORLARNI O'QISH ──────────────────────────────────
wb = load_workbook(FAYL, read_only=True)
ws = wb['kunduzgi']
rows = list(ws.iter_rows(values_only=True))

tyutorlar = []
current = None
for row in rows:
    t_num  = row[0]
    fio_tel = row[1]
    guruh  = row[2]
    if isinstance(t_num, int) and fio_tel and str(fio_tel).strip():
        fio = str(fio_tel).split('\n')[0].strip()
        current = {'num': t_num, 'fio': fio, 'guruhlar': []}
        tyutorlar.append(current)
    elif current and guruh and str(guruh).strip() and not str(guruh).startswith('='):
        g = str(guruh).strip()
        if len(g) > 2 and '-' in g:
            current['guruhlar'].append(g)

print(f"📋 Topildi: {len(tyutorlar)} ta tyutor")
print()

# ── LOGIN YARATISH FUNKSIYASI ─────────────────────────────────────
def fio_to_login(fio):
    """Abdulxamidov Ulugbek -> abdulxamidov_u"""
    parts = fio.replace("'", "").replace("'","").replace("`","").split()
    if len(parts) >= 2:
        familiya = re.sub(r'[^a-zA-Z]', '', parts[0].lower().
            replace('а','a').replace('б','b').replace('в','v').replace('г','g').
            replace('д','d').replace('е','e').replace('ж','j').replace('з','z').
            replace('и','i').replace('й','y').replace('к','k').replace('л','l').
            replace('м','m').replace('н','n').replace('о','o').replace('п','p').
            replace('р','r').replace('с','s').replace('т','t').replace('у','u').
            replace('ф','f').replace('х','x').replace('ц','ts').replace('ч','ch').
            replace('ш','sh').replace('ъ','').replace('ы','i').replace('ь','').
            replace('э','e').replace('ю','yu').replace('я','ya').
            replace('ğ','g').replace('ş','sh').replace('ü','u').replace('ö','o').
            replace('ı','i').replace('ç','ch').replace('â','a').replace('î','i').
            replace('û','u').replace('ô','o').replace("'","").replace("ʼ",""))
        ism_harf = parts[1][0].lower() if parts[1] else ''
        base = f"{familiya}_{ism_harf}"
        return base if base else f"tyutor_{len(tyutorlar)}"
    return f"tyutor_{fio[:8].lower()}"

# ── IMPORT ────────────────────────────────────────────────────────
print("⚙️  Tyutorlar yaratilyapti...\n")

yangi_user = 0
mavjud_user = 0
guruh_topilmadi = []
xatolar = []

natija = []

for t in tyutorlar:
    try:
        fio = t['fio']
        parts = fio.split()

        # Login
        login = fio_to_login(fio)
        # Takrorlanmaslik uchun
        base_login = login
        counter = 1
        while User.objects.filter(username=login).exists():
            login = f"{base_login}{counter}"
            counter += 1

        # Ism familiya
        last_name  = parts[0] if parts else ''
        first_name = ' '.join(parts[1:]) if len(parts) > 1 else ''

        # User yaratish
        if not User.objects.filter(username=base_login).exists():
            user = User.objects.create_user(
                username=login, password='tyutor123',
                first_name=first_name, last_name=last_name
            )
            yangi_user += 1
        else:
            user = User.objects.get(username=base_login)
            mavjud_user += 1

        # Profile
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={'rol': 'tyutor'}
        )
        profile.rol = 'tyutor'
        profile.save()

        # Guruhlarni biriktirish
        guruh_objs = []
        for g_nom in t['guruhlar']:
            g_nom = g_nom.strip()
            try:
                guruh = Guruh.objects.get(nomi=g_nom)
                guruh_objs.append(guruh)
            except Guruh.DoesNotExist:
                # Bo'sh joy bilan qaytadan urini
                try:
                    guruh = Guruh.objects.get(nomi__iexact=g_nom)
                    guruh_objs.append(guruh)
                except Guruh.DoesNotExist:
                    guruh_topilmadi.append(f"{g_nom} ({fio})")

        if guruh_objs:
            profile.guruhlar.set(guruh_objs)

        natija.append({
            'fio': fio, 'login': login,
            'guruhlar': [g.nomi for g in guruh_objs]
        })

        print(f"  ✅ {fio[:40]}")
        print(f"     Login: {login} | Parol: tyutor123")
        print(f"     Guruhlar: {', '.join(t['guruhlar'])}\n")

    except Exception as e:
        xatolar.append(f"{t['fio']}: {e}")

# ── BIRIKTIRILMAGAN GURUHLAR ──────────────────────────────────────
barcha_guruhlar = set(Guruh.objects.values_list('nomi', flat=True))
biriktirilgan = set()
for t in natija:
    biriktirilgan.update(t['guruhlar'])

biriktirilmagan = barcha_guruhlar - biriktirilgan

# ── NATIJA ────────────────────────────────────────────────────────
print("=" * 55)
print("✅ IMPORT YAKUNLANDI!")
print("=" * 55)
print(f"  Yangi tyutor yaratildi : {yangi_user} ta")
print(f"  Allaqachon bor         : {mavjud_user} ta")
print(f"  Biriktirilmagan guruh  : {len(biriktirilmagan)} ta")
print(f"  Xatolar                : {len(xatolar)} ta")
print()
print("  🔑 BARCHA TYUTORLAR PAROLI: tyutor123")
print("=" * 55)

if biriktirilmagan:
    print(f"\n⚠️  Tyutorsiz qolgan {len(biriktirilmagan)} ta guruh:")
    for g in sorted(biriktirilmagan):
        print(f"   - {g}")

if guruh_topilmadi:
    print(f"\n⚠️  Bazada topilmagan guruhlar ({len(guruh_topilmadi)} ta):")
    for g in guruh_topilmadi:
        print(f"   - {g}")

if xatolar:
    print(f"\n❌ Xatolar:")
    for x in xatolar:
        print(f"   {x}")

# Loginlar faylga saqlash
with open('tyutorlar_loginlar.txt', 'w') as f:
    f.write("TYUTORLAR LOGIN VA PAROLLARI\n")
    f.write("=" * 50 + "\n\n")
    for t in natija:
        f.write(f"F.I.Sh : {t['fio']}\n")
        f.write(f"Login  : {t['login']}\n")
        f.write(f"Parol  : tyutor123\n")
        f.write(f"Guruhlar: {', '.join(t['guruhlar'])}\n")
        f.write("-" * 40 + "\n")
print("\n📄 Loginlar 'tyutorlar_loginlar.txt' faylga saqlandi!")
