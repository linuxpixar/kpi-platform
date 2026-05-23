"""
Noto'g'ri yozilgan guruhlarni to'g'rilab tyutorlarga biriktirish
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sertifikat_platform.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Guruh, UserProfile

# Boboyev uchun - ENG -DU-25, ENG GU-23
# Mutalibov uchun - ENG FU-23, ENG BU-23, CHIN AU-23, ENG- FU-24

tuzatishlar = {
    'boboyev_s': ['ENG-DU-25', 'ENG-GU-23'],
    'mutalibov_z': ['ENG-FU-23', 'ENG-BU-23', 'CHIN-AU-23', 'ENG-FU-24'],
}

for login, guruh_nomlari in tuzatishlar.items():
    try:
        user = User.objects.get(username=login)
        profile = user.profile
        
        # Mavjud guruhlarni olish
        mavjud = list(profile.guruhlar.all())
        
        # Yangi guruhlarni qo'shish
        for nom in guruh_nomlari:
            try:
                g = Guruh.objects.get(nomi=nom)
                if g not in mavjud:
                    mavjud.append(g)
                    print(f"  ✅ {login} ga {nom} biriktirildi")
                else:
                    print(f"  ℹ️  {login} da {nom} allaqachon bor")
            except Guruh.DoesNotExist:
                print(f"  ❌ Guruh topilmadi: {nom}")
        
        profile.guruhlar.set(mavjud)
        print(f"\n{login} ning jami guruhlari: {[g.nomi for g in profile.guruhlar.all()]}\n")
        
    except User.DoesNotExist:
        print(f"❌ User topilmadi: {login}")

print("✅ Tayyor!")
