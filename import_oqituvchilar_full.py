"""
O'qituvchilar va kafedra mudirlarini bazaga kiritish.
Ishlatish: python3 import_oqituvchilar_full.py
"""
import os, sys, django, re
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sertifikat_platform.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Fakultet, Kafedra, Oqituvchi, UserProfile

# ── FAKULTETLAR ───────────────────────────────────────────────────
fak_filologiya, _ = Fakultet.objects.get_or_create(nomi='Filologiya fakulteti')
fak_til_tarjima, _ = Fakultet.objects.get_or_create(nomi='Til va tarjima fakulteti')
print(f"✅ Fakultetlar: Filologiya, Til va tarjima")

# ── KAFEDRALAR ────────────────────────────────────────────────────
KAFEDRALAR = {
    # Filologiya fakulteti
    "Ingliz tili va adabiyoti kafedrasi":         fak_filologiya,
    "Nemis va fransuz tillari kafedrasi":          fak_filologiya,
    "O'zbek va sharq tillari kafedrasi":           fak_filologiya,
    # Til va tarjima fakulteti
    "Ingliz tili o'qitish metodikasi kafedrasi":  fak_til_tarjima,
    "Rus filologiyasi kafedrasi":                  fak_til_tarjima,
    "Gumanitar fanlar va jismoniy tarbiya kafedrasi": fak_til_tarjima,
    "Turizm va tarjima kafedrasi":                 fak_til_tarjima,
}

kafedralar = {}
for nom, fak in KAFEDRALAR.items():
    k, created = Kafedra.objects.get_or_create(nomi=nom, defaults={'fakultet': fak, 'kerakli_sert': 2})
    if not created:
        k.fakultet = fak
        k.save()
    kafedralar[nom] = k
    s = "✅ Yaratildi" if created else "ℹ️  Mavjud"
    print(f"  {s}: {nom}")

print(f"\n📚 Jami kafedralar: {len(kafedralar)} ta\n")

# ── KAFEDRALARNI NORMALLASHTIRISH ─────────────────────────────────
def norm_kaf(k):
    k = k.strip()
    m = {
        "Ingliz tili va adabiyoti": "Ingliz tili va adabiyoti kafedrasi",
        "Gumanitar fanlar va jismoniy tarbiya": "Gumanitar fanlar va jismoniy tarbiya kafedrasi",
        "O'zbek va sharq tillari": "O'zbek va sharq tillari kafedrasi",
        "Nemis va fransuz": "Nemis va fransuz tillari kafedrasi",
        "Rus tili va adabiyoti": "Rus filologiyasi kafedrasi",
        "Turizm va tarjima": "Turizm va tarjima kafedrasi",
        "Ingliz tili o'qitish metodikasi": "Ingliz tili o'qitish metodikasi kafedrasi",
    }
    return m.get(k, k)

# ── O'QITUVCHILAR MA'LUMOTLARI ────────────────────────────────────
OQITUVCHILAR = [
    # FIO, lavozim, kafedra, mudirmi
    ("Amanov Akmal Aripjonovich","Kafedra mudiri, Dotsent","Ingliz tili o'qitish metodikasi kafedrasi",True),
    ("Jakbarova Nasibaxon Po'latjonovana","O'qituvchi (PhD)","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("Abdullayev Nurillo Abdullo o'g'li","O'qituvchi-stajyor","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("Erkulova Feruza Melikuziyevna","Dotsent, PhD","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("Tursunaliyev Nozimjon Nabijon o'g'li","O'qituvchi-stajyor","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("Tojiboyev G'ayratjon Shovdorovich","Dotsent, PhD","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("Yuldasheva Ma'mura Boqijonovna","Katta o'qituvchi","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("Xoldarova Soxiba Gulomjon qizi","O'qituvchi-stajyor","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("Boboyeva Muazzam Narimonovna","O'qituvchi-stajyor","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("Pulatov Doniyor Sayfulla o'g'li","O'qituvchi-stajyor","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("Po'latov Muxammadyusuf muxammad o'g'li","O'qituvchi","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("Kenjayev Azizbek Rustamjon o'g'li","O'qituvchi-stajyor","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("Abdullayeva Madinabonu Akmaljon qizi","Katta o'qituvchi","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("Rejabova Nigoraxon Muxammadikrom qizi","O'qituvchi-stajyor","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("Axmadjonova Odina Anvarjon qizi","O'qituvchi-stajyor","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("Abdujalilova Mashxuraxon Alisher qizi","O'qituvchi-stajyor (o'rindosh)","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("Baxriddinov Azizbek Xayrullo o'g'li","O'qituvchi (o'rindosh)","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("Bozorova Gulshoda Shavkatjon qizi","O'qituvchi-stajyor (o'rindosh)","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("Komilova Muxarramxon Nosirjon qizi","O'qituvchi-stajyor (o'rindosh)","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("Mamadjanova Nozima Adxamovna","O'qituvchi-stajyor (o'rindosh)","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("Mamadjonova Shoxida Nemat qizi","O'qituvchi-stajyor (o'rindosh)","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("Mamajonov Rustamjon Isroiljon o'g'li","O'qituvchi (o'rindosh)","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("Murodullayev Behzod Boxodir o'g'li","O'qituvchi-stajyor (o'rindosh)","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("Rahimjonova Muhtasar Rasuljon qizi","O'qituvchi-stajyor (o'rindosh)","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("To'xtanazarov Asadbek Olimjon o'g'li","O'qituvchi-stajyor (o'rindosh)","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("Xamidullayeva Nigora Murodillo qizi","O'qituvchi-stajyor (o'rindosh)","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("Xaydarova Sarvinoz Zuxriddinovna","O'qituvchi-stajyor (o'rindosh)","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("Yuldasheva Maxliyoxon Ahmatjon qizi","O'qituvchi-stajyor (o'rindosh)","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("Ergashev Alisher Rasuljon o'g'li","O'qituvchi-stajyor (o'rindosh)","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("Xoshimova Diyora Azamjon qizi","O'qituvchi-stajyor (o'rindosh)","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("Ibragimov Jasur","O'qituvchi (o'rindosh)","Ingliz tili o'qitish metodikasi kafedrasi",False),
    ("Ibragimov Javoxir","O'qituvchi (o'rindosh)","Ingliz tili o'qitish metodikasi kafedrasi",False),
    # Ingliz tili va adabiyoti
    ("Tursunov Muxammadyusuf Alisher o'g'li","Kafedra mudiri, PhD","Ingliz tili va adabiyoti kafedrasi",True),
    ("Ismoiljonov Shuxratjon Bekmirza o'g'li","O'qituvchi","Ingliz tili va adabiyoti kafedrasi",False),
    ("A'zamov Sayfulbot Maxamadaliyevich","Katta o'qituvchi","Ingliz tili va adabiyoti kafedrasi",False),
    ("Axmadjonov Tursunpo'lat Axmadjon o'g'li","Katta o'qituvchi","Ingliz tili va adabiyoti kafedrasi",False),
    ("Umrzaqov Islomjon Isroilovich","Dotsent, PhD","Ingliz tili va adabiyoti kafedrasi",False),
    ("Xujanazarova Nozima Omonjonovna","O'qituvchi-stajyor","Ingliz tili va adabiyoti kafedrasi",False),
    ("Madmusayev Jaxongir Muxtorali o'g'li","Katta o'qituvchi","Ingliz tili va adabiyoti kafedrasi",False),
    ("Dadaboyev Olimjon Ortiqovich","Dotsent, PhD","Ingliz tili va adabiyoti kafedrasi",False),
    ("Tursunova Moxira Ilxomjonovna","O'qituvchi","Ingliz tili va adabiyoti kafedrasi",False),
    ("Boqiyev Nurali Abdurashid o'g'li","O'qituvchi-stajyor","Ingliz tili va adabiyoti kafedrasi",False),
    ("Turg'unova Dilnoza G'ofurjon qizi","O'qituvchi","Ingliz tili va adabiyoti kafedrasi",False),
    ("Nasrullayeva Umida Baxrom qizi","O'qituvchi","Ingliz tili va adabiyoti kafedrasi",False),
    ("Madaminov G'olibjon G'ofurjon o'g'li","O'qituvchi-stajyor","Ingliz tili va adabiyoti kafedrasi",False),
    ("Mashrabova Dilnoza Avazxon qizi","O'qituvchi-stajyor","Ingliz tili va adabiyoti kafedrasi",False),
    ("Xoshimova Maftuna Qodirali qizi","O'qituvchi","Ingliz tili va adabiyoti kafedrasi",False),
    ("Ismoilova Zarnigor Raximjon qizi","O'qituvchi-stajyor","Ingliz tili va adabiyoti kafedrasi",False),
    ("G'aniyeva Barchinoy Mahmud qizi","O'qituvchi-stajyor","Ingliz tili va adabiyoti kafedrasi",False),
    ("Toshpulatov Bexzod Bekmurod o'g'li","O'qituvchi","Ingliz tili va adabiyoti kafedrasi",False),
    ("Obilov Ibroximjon Vaxobjon o'g'li","O'qituvchi-stajyor","Ingliz tili va adabiyoti kafedrasi",False),
    ("Qoraboyev Mirzoxid Xoshimovich","Dotsent","Ingliz tili va adabiyoti kafedrasi",False),
    ("Qodirov Azamat Muxriddinovich","O'qituvchi","Ingliz tili va adabiyoti kafedrasi",False),
    ("Xabibullayev Xakimxo'ja Xamidulla o'g'li","O'qituvchi-stajyor","Ingliz tili va adabiyoti kafedrasi",False),
    ("Abdug'aniyeva Xusnidaxon Sanjarbek qizi","O'qituvchi-stajyor (o'rindosh)","Ingliz tili va adabiyoti kafedrasi",False),
    ("Chinaqov Abdulaxad Mo'minjon o'g'li","O'qituvchi-stajyor (o'rindosh)","Ingliz tili va adabiyoti kafedrasi",False),
    ("Mamasharipova Mohinur Ma'rufjon qizi","O'qituvchi-stajyor (o'rindosh)","Ingliz tili va adabiyoti kafedrasi",False),
    ("Mirsadullayev Miravaz Mirmuslim o'g'li","Katta o'qituvchi (o'rindosh)","Ingliz tili va adabiyoti kafedrasi",False),
    ("Olimova Odina To'xtasin qizi","O'qituvchi-stajyor (o'rindosh)","Ingliz tili va adabiyoti kafedrasi",False),
    ("Saydamatova Dilafro'z Xamidullo qizi","O'qituvchi-stajyor (o'rindosh)","Ingliz tili va adabiyoti kafedrasi",False),
    ("Xakimova Mohichexra Abdulboqi qizi","O'qituvchi-stajyor (o'rindosh)","Ingliz tili va adabiyoti kafedrasi",False),
    ("Xolmirzayev Baxtiyor Mirzamaxmudovich","Dotsent (o'rindosh)","Ingliz tili va adabiyoti kafedrasi",False),
    ("Egamova Nigora Ustamirzayevna","O'qituvchi-stajyor (o'rindosh)","Ingliz tili va adabiyoti kafedrasi",False),
    ("Axundjanov Baxodir Zafarovich","O'qituvchi (o'rindosh)","Ingliz tili va adabiyoti kafedrasi",False),
    ("Najmiddinova Shaxnoza Abdullajon qizi","O'qituvchi-stajyor (o'rindosh)","Ingliz tili va adabiyoti kafedrasi",False),
    ("Raxmonova Zebunisso Anvarjon qizi","Katta o'qituvchi (o'rindosh)","Ingliz tili va adabiyoti kafedrasi",False),
    # Nemis va fransuz tillari
    ("Tursunov Akmaljon Xamidjonovich","Kafedra mudiri, Dotsent","Nemis va fransuz tillari kafedrasi",True),
    ("Tursunov Xusanboy Burgutaliyevich","Dotsent, PhD","Nemis va fransuz tillari kafedrasi",False),
    ("Abdullajonov Akmalxon Axmadjonovich","Dotsent","Nemis va fransuz tillari kafedrasi",False),
    ("Madolimov Xusanboy Shuxratovich","Katta o'qituvchi","Nemis va fransuz tillari kafedrasi",False),
    ("Satvoldiyeva Ma'mura Maxammadaminovna","O'qituvchi","Nemis va fransuz tillari kafedrasi",False),
    ("Atamirzayeva E'zoza Bekmirzayevna","Katta o'qituvchi","Nemis va fransuz tillari kafedrasi",False),
    ("Tursunov Zoxidjon Zokirjonovich","Katta o'qituvchi","Nemis va fransuz tillari kafedrasi",False),
    ("Yusupova Umida Inomovna","O'qituvchi","Nemis va fransuz tillari kafedrasi",False),
    ("Mirvaliyev Furqat Shuxratovich","O'qituvchi-stajyor","Nemis va fransuz tillari kafedrasi",False),
    ("Tursunova Zarnigor","O'qituvchi-stajyor","Nemis va fransuz tillari kafedrasi",False),
    ("Raximov Xusniddin Tojakmatovich","Katta o'qituvchi","Nemis va fransuz tillari kafedrasi",False),
    ("Raxmonova Maloxat Abdulxamid qizi","O'qituvchi-stajyor","Nemis va fransuz tillari kafedrasi",False),
    ("Dodobayev Saminjon Mamajonovich","Katta o'qituvchi","Nemis va fransuz tillari kafedrasi",False),
    ("Abduraxmonova Dilraboxon Kodirjonovna","Katta o'qituvchi (o'rindosh)","Nemis va fransuz tillari kafedrasi",False),
    ("Bobaxonov Muhammadjon Yaxyayevich","Katta o'qituvchi (o'rindosh)","Nemis va fransuz tillari kafedrasi",False),
    ("Mamadjonov Valijon Alixanovich","O'qituvchi (o'rindosh)","Nemis va fransuz tillari kafedrasi",False),
    ("Tillabayeva Zuxraxon Xamidillo qizi","O'qituvchi-stajyor (o'rindosh)","Nemis va fransuz tillari kafedrasi",False),
    ("Todjixodjayev Muso Muydinbayevich","Dotsent (o'rindosh)","Nemis va fransuz tillari kafedrasi",False),
    # O'zbek va sharq tillari
    ("Abdurasulova Umida Sadullayevna","Kafedra mudiri, Dotsent","O'zbek va sharq tillari kafedrasi",True),
    ("Yandashev Zikirjon Xolmatjon o'g'li","O'qituvchi-stajyor","O'zbek va sharq tillari kafedrasi",False),
    ("No'monxonova Muattarxon Nosirxon qizi","O'qituvchi-stajyor","O'zbek va sharq tillari kafedrasi",False),
    ("Sobirova Nasiba Avazovna","O'qituvchi","O'zbek va sharq tillari kafedrasi",False),
    ("Xo'janazarova Nazira Omonjonovna","O'qituvchi","O'zbek va sharq tillari kafedrasi",False),
    ("Baqoyev Navro'zjon Abdullo o'g'li","O'qituvchi-stajyor","O'zbek va sharq tillari kafedrasi",False),
    ("Erkinov Ahrorbek To'lqinboy o'g'li","O'qituvchi-stajyor","O'zbek va sharq tillari kafedrasi",False),
    ("Usmonova Soxiba","O'qituvchi-stajyor","O'zbek va sharq tillari kafedrasi",False),
    ("Ibragimov Sodiqjon Suyarqul o'g'li","O'qituvchi","O'zbek va sharq tillari kafedrasi",False),
    ("Orifjonov Botirjon Boxodir o'g'li","O'qituvchi-stajyor (o'rindosh)","O'zbek va sharq tillari kafedrasi",False),
    ("Raximov Xasanboy Komiljonovich","O'qituvchi-stajyor (o'rindosh)","O'zbek va sharq tillari kafedrasi",False),
    ("Salimova Sohiba Bazarboyevna","O'qituvchi-stajyor (o'rindosh)","O'zbek va sharq tillari kafedrasi",False),
    # Rus filologiyasi
    ("Gafarova Lola Salimbekovna","Kafedra mudiri, Dotsent","Rus filologiyasi kafedrasi",True),
    ("Mirzanazarova Aziza Mirzaabdullayevna","Katta o'qituvchi","Rus filologiyasi kafedrasi",False),
    ("Kazakova Ra'no Mashrabayevna","Katta o'qituvchi, PhD","Rus filologiyasi kafedrasi",False),
    ("Kamalova Kadriya Fyodorovna","Dotsent","Rus filologiyasi kafedrasi",False),
    ("Kazakbayeva Saodat Inomiddinovna","Dotsent","Rus filologiyasi kafedrasi",False),
    ("Akmalova Dildora Toxirovna","Dotsent","Rus filologiyasi kafedrasi",False),
    ("Mamadaliyeva Saida Vaxiddinovna","O'qituvchi","Rus filologiyasi kafedrasi",False),
    ("Abdusamatov Mavlonjon Mukarramjon o'g'li","O'qituvchi","Rus filologiyasi kafedrasi",False),
    ("Sobirov Azizbek Baxodir o'g'li","O'qituvchi-stajyor","Rus filologiyasi kafedrasi",False),
    ("Mamasodiqova Maxzuna Jalol qizi","O'qituvchi-stajyor","Rus filologiyasi kafedrasi",False),
    ("Abdullayeva Iqbola Moxirovna","Katta o'qituvchi","Rus filologiyasi kafedrasi",False),
    ("Yusupova Ra'noxon Kamolhanovna","Katta o'qituvchi","Rus filologiyasi kafedrasi",False),
    ("Yo'ldoshev Muxammad To'lqinboy o'g'li","O'qituvchi-stajyor","Rus filologiyasi kafedrasi",False),
    ("Sharofov Javlon Rafiqjon o'g'li","O'qituvchi-stajyor","Rus filologiyasi kafedrasi",False),
    ("Mirzakbarova Sevda","O'qituvchi-stajyor","Rus filologiyasi kafedrasi",False),
    ("Akramova Elmira Irkinovna","Katta o'qituvchi (o'rindosh)","Rus filologiyasi kafedrasi",False),
    ("Chjen Yelena Vitalyevna","Dotsent (o'rindosh)","Rus filologiyasi kafedrasi",False),
    ("Fayzullayeva Xurshidaxon Erkinjon qizi","Katta o'qituvchi (o'rindosh)","Rus filologiyasi kafedrasi",False),
    ("Abdullayeva Saidaxon Nuritdinovna","Dotsent (o'rindosh)","Rus filologiyasi kafedrasi",False),
    # Gumanitar fanlar
    ("Mirzaxalov Sardorbek Jamoliddinovich","Kafedra mudiri, PhD","Gumanitar fanlar va jismoniy tarbiya kafedrasi",True),
    ("Abduxolikova Nasiba Alijonovna","Dotsent, PhD","Gumanitar fanlar va jismoniy tarbiya kafedrasi",False),
    ("Xolmatova Saida Voxobjonovna","Dotsent","Gumanitar fanlar va jismoniy tarbiya kafedrasi",False),
    ("Sodiqov Abduxalil Abdukaxxar o'g'li","O'qituvchi-stajyor","Gumanitar fanlar va jismoniy tarbiya kafedrasi",False),
    ("Po'latov Maxmudjon Turgunovich","O'qituvchi","Gumanitar fanlar va jismoniy tarbiya kafedrasi",False),
    ("Xo'jamov Muzaffar Rasuljonovich","Katta o'qituvchi","Gumanitar fanlar va jismoniy tarbiya kafedrasi",False),
    ("Djalolov Baxrom Djamolovich","O'qituvchi","Gumanitar fanlar va jismoniy tarbiya kafedrasi",False),
    ("Atabayeva Nargisa Nabijonovna","O'qituvchi","Gumanitar fanlar va jismoniy tarbiya kafedrasi",False),
    ("Axmedova Dilrabo Sadullayevna","O'qituvchi","Gumanitar fanlar va jismoniy tarbiya kafedrasi",False),
    ("Mirzaraxmonova Maftuna Ibrohimjon qizi","O'qituvchi-stajyor","Gumanitar fanlar va jismoniy tarbiya kafedrasi",False),
    ("Ergashev Jaxongir Abdurasul o'g'li","O'qituvchi-stajyor","Gumanitar fanlar va jismoniy tarbiya kafedrasi",False),
    ("Ismoilov Temur","Professor","Gumanitar fanlar va jismoniy tarbiya kafedrasi",False),
    ("Badalov Avazbek","O'qituvchi-stajyor","Gumanitar fanlar va jismoniy tarbiya kafedrasi",False),
    ("Nurmuxammadova Yoqut Nurmuxammadjonovna","O'qituvchi-stajyor","Gumanitar fanlar va jismoniy tarbiya kafedrasi",False),
    ("G'anijonov Shohijaxon G'ayratjon o'g'li","O'qituvchi-stajyor (o'rindosh)","Gumanitar fanlar va jismoniy tarbiya kafedrasi",False),
    ("Orifjonov Botirjon Boxodir o'g'li","O'qituvchi-stajyor (o'rindosh)","Gumanitar fanlar va jismoniy tarbiya kafedrasi",False),
    ("Turg'unov Sherzod Abduvositovich","O'qituvchi-stajyor (o'rindosh)","Gumanitar fanlar va jismoniy tarbiya kafedrasi",False),
    # Turizm va tarjima
    ("Ermirzayev Abbos Vaxobjonovich","Kafedra mudiri, Dotsent","Turizm va tarjima kafedrasi",True),
    ("Dosbayeva Nargiza Turg'unpo'latovna","Professor, DSc","Turizm va tarjima kafedrasi",False),
    ("Botirova Palina","Dotsent, PhD","Turizm va tarjima kafedrasi",False),
    ("Mirzayev Shavkat Nasibjon o'g'li","O'qituvchi","Turizm va tarjima kafedrasi",False),
    ("Jakbarova Iroda Badriddin qizi","O'qituvchi-stajyor","Turizm va tarjima kafedrasi",False),
    ("Xoliqov Zoxidjon Olimjonovich","Katta o'qituvchi","Turizm va tarjima kafedrasi",False),
    ("Tulanboyeva Dildora Tulkinjon qizi","O'qituvchi","Turizm va tarjima kafedrasi",False),
    ("Valijonov Sherzod Abdug'ani o'g'li","Katta o'qituvchi","Turizm va tarjima kafedrasi",False),
    ("Nematova Maftuna Mirzajon qizi","Katta o'qituvchi","Turizm va tarjima kafedrasi",False),
    ("Salavatova Liliya Enverovna","O'qituvchi","Turizm va tarjima kafedrasi",False),
    ("Mamajonov Ravshanjon Isroiljon o'g'li","O'qituvchi (o'rindosh)","Turizm va tarjima kafedrasi",False),
    ("Qambaraliyev Behruz Ahmadjon o'g'li","O'qituvchi-stajyor (o'rindosh)","Turizm va tarjima kafedrasi",False),
    ("Raxmatov Jaxongirmirzo G'ayratjon o'g'li","O'qituvchi-stajyor (o'rindosh)","Turizm va tarjima kafedrasi",False),
]

# ── LOGIN YARATISH ────────────────────────────────────────────────
def make_login(fio):
    parts = fio.replace("'","").replace("'","").replace("`","").split()
    if len(parts) >= 2:
        fam = re.sub(r'[^a-z]', '', parts[0].lower()
            .replace('а','a').replace('б','b').replace('в','v').replace('г','g')
            .replace('д','d').replace('е','e').replace('ж','j').replace('з','z')
            .replace('и','i').replace('й','y').replace('к','k').replace('л','l')
            .replace('м','m').replace('н','n').replace('о','o').replace('п','p')
            .replace('р','r').replace('с','s').replace('т','t').replace('у','u')
            .replace('ф','f').replace('х','x').replace('ч','ch').replace('ш','sh')
            .replace('ъ','').replace('ы','i').replace('ь','').replace('э','e')
            .replace('ю','yu').replace('я','ya').replace('ğ','g').replace('ş','sh')
            .replace('ü','u').replace('ö','o').replace('ı','i').replace('ç','ch')
            .replace("'","").replace("ʼ","").replace("'",""))
        ini = parts[1][0].lower() if parts[1] else ''
        return f"{fam}_{ini}" if fam else f"user_{len(fam)}"
    return 'user'

# ── IMPORT ────────────────────────────────────────────────────────
print("⚙️  O'qituvchilar kiritilmoqda...\n")
yangi_oqit = 0
yangi_user = 0
mudirlar_log = []

for fio, lavozim, kafedra_nom, mudirmi in OQITUVCHILAR:
    fio = fio.strip()
    if not fio or len(fio) < 3:
        continue
    kafedra = kafedralar.get(kafedra_nom)
    if not kafedra:
        print(f"  ⚠️  Kafedra topilmadi: {kafedra_nom}")
        continue

    # O'qituvchi
    if not Oqituvchi.objects.filter(fio=fio, kafedra=kafedra).exists():
        Oqituvchi.objects.create(fio=fio, kafedra=kafedra, lavozim=lavozim)
        yangi_oqit += 1

    # Kafedra mudiri uchun user
    if mudirmi:
        login = make_login(fio)
        base = login
        i = 1
        while User.objects.filter(username=login).exists():
            login = f"{base}{i}"; i += 1

        parts = fio.split()
        u = User.objects.create_user(login, '', 'mudiri123')
        u.last_name  = parts[0] if parts else ''
        u.first_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
        u.save()

        pr = UserProfile.objects.create(user=u, rol='kafedra_mudiri', kafedra=kafedra)
        kafedra.mudiri = u
        kafedra.save()
        yangi_user += 1
        mudirlar_log.append((fio, login, kafedra_nom))
        print(f"  👤 {fio}")
        print(f"     Login: {login} | Parol: mudiri123")
        print(f"     Kafedra: {kafedra_nom}\n")

# ── NATIJA ────────────────────────────────────────────────────────
print("=" * 58)
print("✅ IMPORT YAKUNLANDI!")
print("=" * 58)
print(f"  Fakultetlar    : 2 ta")
print(f"  Kafedralar     : {Kafedra.objects.count()} ta")
print(f"  O'qituvchilar  : {Oqituvchi.objects.count()} ta (yangi: {yangi_oqit})")
print(f"  Kafedra mudirlari: {yangi_user} ta")
print()
print("  🔑 KAFEDRA MUDIRLARI PAROLI: mudiri123")
print("=" * 58)

# Loginlar faylga
with open('mudirlar_loginlar.txt', 'w') as f:
    f.write("KAFEDRA MUDIRLARI LOGIN VA PAROLLARI\n")
    f.write("=" * 50 + "\n\n")
    for fio, login, kaf in mudirlar_log:
        f.write(f"F.I.Sh  : {fio}\n")
        f.write(f"Login   : {login}\n")
        f.write(f"Parol   : mudiri123\n")
        f.write(f"Kafedra : {kaf}\n")
        f.write("-" * 40 + "\n")

print("\n📄 Loginlar 'mudirlar_loginlar.txt' faylga saqlandi!")
