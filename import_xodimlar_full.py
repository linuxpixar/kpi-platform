"""
Barcha xodimlar, o'qituvchilar va kafedra mudirlarini bazaga kiritish.
Ishlatish: python3 import_xodimlar_full.py
"""
import os, sys, django, re
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sertifikat_platform.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Fakultet, Kafedra, Bolim, Oqituvchi, Xodim, UserProfile

# ── MA'LUMOTLAR ───────────────────────────────────────────────────
# Format: (FIO, bo'lim/kafedra, lavozim)
XODIMLAR_DATA = """Lutfullayev Po'latxon Muxibullayevich	Rahbariyat	Prorektor
Nishonov Xayrulla Xolmirzayevich	Rahbariyat	Prorektor
Yakubbayev Murodilla Marufovich	Rahbariyat	Prorektor
Turg'unov Mansurjon Maxmudjon o'g'li	Rahbariyat	Boshqarma boshlig'i
Shokirov Abduraxmonjon Abduvalijonovich	Rahbariyat	Rektor maslaxatchisi
Sobirov Boqijon Abdullayevich	Rahbariyat	Bosh muhandis
Abdug'opporova Laylo Valijon qizi	Mamuriyat	Psixolog
Ikramov Alisher Shukrullayevich	Mamuriyat	Bosh mutaxassis
Abdulxayev Abduvali Abdurayimjon o'g'li	Mamuriyat	Bo'lim boshlig'i
Muxsiddinov Jaloloddin Ruxiddin o'g'li	Mamuriyat	Inspektor
Turg'unova Madina Abdulxamidovna	Mamuriyat	Xodimlar bo'yicha muhandis
Muydinov Mansurbek Ilhomjon o'g'li	Mamuriyat	Bo'lim boshlig'i
Xojiyev Nodirxon Qosimjon o'g'li	Mamuriyat	Bosh mutaxassis
Urayimjonov Nurmuxammad	Mamuriyat	Bino komendanti
Qutbiddinova Sabohat	Mamuriyat	Ish yurituvchi
Valiyev Qobiljon Obidjonovich	Mamuriyat	Bo'lim boshlig'i
Murodullayev Ubaydullo Abdullajon o'g'li	Mamuriyat	Bosh mutaxassis
Qo'ziboyev Baxtiyor Xamidjonovich	Mamuriyat	Bosh auditor
Anvarjonov Azamat Ne'matjon o'g'li	Mamuriyat	Bosh buxgalter
Yusupov Dilmurod Farxodovich	Mamuriyat	Bosh buxgalter o'rinbosari
Usmonqulova Saida Xolmatjonovna	Mamuriyat	Buxgalter
Sattorov Nurilla Qobiljon o'g'li	Mamuriyat	Bosh mutaxassis
Abdulboriyev Shaxboz Abdulboriyevich	Mamuriyat	Buxgalter
Abduraximov Murodjon Abdunazarovich	Mamuriyat	Buxgalter
Xayitmatov Elmurod Xusanovich	Mamuriyat	Bo'lim boshlig'i
Ne'matov Abdullo Nazirjon o'g'li	Mamuriyat	Iqtisodchi
Isoqov Zafarjon Zokirjonovich	Mamuriyat	Bo'lim boshlig'i
Ismoilov Doston Ismon o'g'li	Mamuriyat	Bo'lim boshlig'i
Dadaboyev Farxodjon Ibroximovich	Mamuriyat	Menejer
Xomidov Abdug'affor Axmadjonovich	Mamuriyat	Menejer
Ne'matov Jaxongir Munosiddin o'g'li	Mamuriyat	Menejer
Kamoliddinov Murodjon Burxoniddin o'g'li	Mamuriyat	Menejer
Ibragimov Doniyor Xoshimjonovich	Mamuriyat	Bo'lim boshlig'i
Jabborov Elmurod Qambaraliyevich	Mamuriyat	Menejer
Mansurov Fayzullo Saydullayevich	Mamuriyat	Menejer
Yuldasheva Dilbarxon Ibroximjon qizi	Mamuriyat	Menejer
Isomiddinov Eldorbek Botirovich	Mamuriyat	Dekan
Soxibjonov Zoxidjon Soxibjon o'g'li	Mamuriyat	Dekan o'rinbosari
Ne'matjonov Sharifjon Rustamjonovich	Mamuriyat	Dekan o'rinbosari
Boboxonova Dilshoda Oripxon qizi	Mamuriyat	Tyutor
Yuldashyeva Dilnoza Sharifjonovna	Mamuriyat	Tyutor
Yuldosheva Oydinxon Baxromjonovna	Mamuriyat	Tyutor
G'ulomjonov G'ofurjon G'ulomjon o'g'li	Mamuriyat	Tyutor
Azimjonova Iroda Abdumutal qizi	Mamuriyat	Kabinet mudiri
Misirov Soxibjon Abdupattayevich	Mamuriyat	Dekan
Rustamaliyev Mirjalol Xayrullo o'g'li	Mamuriyat	Dekan o'rinbosari
Toshpulatov Bexzod Bekmurod o'g'li	Mamuriyat	Dekan o'rinbosari
Abdualiyev Xamidulla Toxirjonovich	Mamuriyat	Dekan o'rinbosari
Qobilova Nodira Maxmutdjonovna	Mamuriyat	Ish yurituvchi
Abdulxamidov Ulug'bek Abdulpatto o'g'li	Mamuriyat	Tyutor
Abdurazzoqov Jaxongir Baxodir o'g'li	Mamuriyat	Tyutor
Usmanova Dilorom Ne'matovna	Mamuriyat	Tyutor
Xodjiboyeva Muqaddas Xakimjonovna	Mamuriyat	Tyutor
Jo'raboyeva Sevara Xusnitdin qizi	Mamuriyat	Tyutor
O'rinova Dildora Abduraxmonovna	Mamuriyat	Tyutor
Mirg'aniyeva Muxabbat Ortiqbayevna	Mamuriyat	Tyutor
Jurayev Azizbek Azimjonovich	Mamuriyat	Tyutor
Ergashboyev Nizomjon Numonjon o'g'li	Mamuriyat	Tyutor
Usmonova Moxira Maxamadjon qizi	Mamuriyat	Tyutor
Soliyev Umidjon Yulchivoyevich	Mamuriyat	Boshqarma boshlig'i
Ayturayev Majid Mavlanxanovich	Mamuriyat	Bo'lim boshlig'i
Ziyoviddinov Mirjalol G'ofurjon o'g'li	Mamuriyat	Bo'lim boshlig'i
Tojiboyev Akramjon Rasuljon o'g'li	Mamuriyat	Menejer
Umarxonov Nurillo Ismatullayevich	Mamuriyat	Bo'lim boshlig'i
G'anijonov Azamat Doniyor o'g'li	Mamuriyat	Bosh mutaxassis
Ibroximov Ozodbek Shuxrat o'g'li	Mamuriyat	Uslubchi
Sobirjonov Elmurod Obidjon o'g'li	Mamuriyat	Bo'lim boshlig'i
Usmonov Shoxruxbek Shavkatjon o'g'li	Mamuriyat	Markaz boshlig'i
Sharibjonov Ziyodulla Zokirjon o'g'li	Mamuriyat	Tarmoq administratori
Xamidullayev Shaxzodbek	Mamuriyat	Veb-dizayner
Raxmatov Jaxongir	Mamuriyat	Tarmoq administratori
Raximova Nigoraxon Obidjanovna	Mamuriyat	Bo'lim boshlig'i
Xoshimov Muzaffar	Mamuriyat	Ilmiy tadqiqot muhandisi
Sulaymanov Asatullo Usubxanovich	Mamuriyat	Rektor yordamchisi
Samixanov Baxodir Minavarxanovich	Mamuriyat	Bo'lim boshlig'i
Xolmirzayeva Dilafro'z G'ulomjon qizi	Mamuriyat	Tarbiyachi-pedagog
Qaxxorova Marg'ubaxon Xakimjonovna	Mamuriyat	Kutubxonachi
Turg'unova Dilorom Nasimjonovna	Mamuriyat	Kutubxonachi
Azizova Nodiraxon Nosirjonovna	Mamuriyat	Kutubxonachi
Maxmurxonova Feruza Asadovna	Mamuriyat	Bosh mutaxassis
Abdullayeva Irodaxon Sobirjon qizi	Mamuriyat	Kutubxonachi
Kenjayeva Nafisa Xoshimjonovna	Mamuriyat	Kutubxonachi
Sharofiddinov Maxmudjon Mashrabjon o'g'li	Mamuriyat	Bo'lim boshlig'i
Abdug'afforov Axrorbek Adxamjon o'g'li	Mamuriyat	Bo'lim boshlig'i
Usmanova Go'zal Ulug'bek qizi	Mamuriyat	Kotib-ish yurituvchi
Majidova Xulkaroy G'anijonovna	Mamuriyat	Kabinet mudiri
Odilova Sayyora Isaqovna	Mamuriyat	Kabinet mudiri
Tojiboyeva Manzura Raxmatjonovna	Mamuriyat	Kabinet mudiri
Makamova Dilfuza Gaybillayevna	Mamuriyat	Kabinet mudiri
Ibragimova Noila Ibragim qizi	Mamuriyat	Matbuot kotibi
Nabijonova Durdona	Mamuriyat	Uslubchi
Odilova Moxidil	Mamuriyat	Yordamchi ishchi
Nuritdinova Xurshida Nuridinovna	Mamuriyat	Tyutor
Abdurahmonov Sanjarbek Inomjon o'g'li	Mamuriyat	Uslubchi
Xayrullayev Jaxongir Jamolxon o'g'li	Mamuriyat	Devonxona mudiri
Obidjonov Azizbek Oqiljon o'g'li	Mamuriyat	Uslubchi
Bobayev Sodiqjon Isomiddinovich	Mamuriyat	Tyutor
Abdullayev Akbar Xabibulla o'g'li	Mamuriyat	Uslubchi
Ergasheva Yulduzxon Sobitovna	Mamuriyat	Psixolog
Qobilova Shoira Najmiddin qizi	Texnik	Farrosh"""

OQITUVCHILAR_DATA = """Amanov Akmal Aripjonovich	Ingliz tili o'qitish metodikasi kafedrasi	Kafedra mudiri
Jakbarova Nasibaxon Po'latjonovana	Ingliz tili o'qitish metodikasi kafedrasi	O'qituvchi-stajer
Abdullayev Nurillo Abdullo o'g'li	Ingliz tili o'qitish metodikasi kafedrasi	O'qituvchi
Erkulova Feruza Melikuziyevna	Ingliz tili o'qitish metodikasi kafedrasi	Dotsent
Tursunaliyev Nozimjon Nabijon o'g'li	Ingliz tili o'qitish metodikasi kafedrasi	O'qituvchi-stajer
Tojiboyev G'ayratjon Shovdorovich	Ingliz tili o'qitish metodikasi kafedrasi	Dotsent
Yuldasheva Ma'mura Boqijonovna	Ingliz tili o'qitish metodikasi kafedrasi	Katta o'qituvchi
Xoldarova Soxiba Gulomjon qizi	Ingliz tili o'qitish metodikasi kafedrasi	O'qituvchi-stajer
Boboyeva Muazzam Narimonovna	Ingliz tili o'qitish metodikasi kafedrasi	O'qituvchi
Pulatov Doniyor Sayfulla o'g'li	Ingliz tili o'qitish metodikasi kafedrasi	O'qituvchi-stajer
Po'latov Muxammadyusuf muxammad o'g'li	Ingliz tili o'qitish metodikasi kafedrasi	Assistent
Kenjayev Azizbek Rustamjon o'g'li	Ingliz tili o'qitish metodikasi kafedrasi	Bosh mutaxassis
Abdullayeva Madinabonu Akmaljon qizi	Ingliz tili o'qitish metodikasi kafedrasi	Katta o'qituvchi
Ismoiljonov Shuxratjon Bekmirza o'g'li	Ingliz tili o'qitish metodikasi kafedrasi	Katta o'qituvchi
Rejabova Nigoraxon Muxammadikrom qizi	Ingliz tili o'qitish metodikasi kafedrasi	O'qituvchi-stajer
Axmadjonova Odina Anvarjon qizi	Ingliz tili o'qitish metodikasi kafedrasi	O'qituvchi-stajer
Mirzaxalov Sardorbek Jamoliddinovich	Gumanitar fanlar va jismoniy tarbiya kafedrasi	Kafedra mudiri
Abduxolikova Nasiba Alijonovna	Gumanitar fanlar va jismoniy tarbiya kafedrasi	Katta o'qituvchi
Xolmatova Saida Voxobjonovna	Gumanitar fanlar va jismoniy tarbiya kafedrasi	Dotsent v.b
Sodiqov Abduxalil Abdukaxxar o'g'li	Gumanitar fanlar va jismoniy tarbiya kafedrasi	O'qituvchi-stajer
Po'latov Maxmudjon Turgunovich	Gumanitar fanlar va jismoniy tarbiya kafedrasi	Katta o'qituvchi
Xo'jamov Muzaffar Rasuljonovich	Gumanitar fanlar va jismoniy tarbiya kafedrasi	Katta o'qituvchi
Djalolov Baxrom Djamolovich	Gumanitar fanlar va jismoniy tarbiya kafedrasi	Katta o'qituvchi
Atabayeva Nargisa Nabijonovna	Gumanitar fanlar va jismoniy tarbiya kafedrasi	Assistent
Axmedova Dilrabo Sadullayevna	Gumanitar fanlar va jismoniy tarbiya kafedrasi	O'qituvchi
Mirzaraxmonova Maftuna Ibrohimjon qizi	Gumanitar fanlar va jismoniy tarbiya kafedrasi	O'qituvchi
Ergashev Jaxongir Abdurasul o'g'li	Gumanitar fanlar va jismoniy tarbiya kafedrasi	O'qituvchi-stajer
Badalov Avazbek	Gumanitar fanlar va jismoniy tarbiya kafedrasi	O'qituvchi
Nurmuxammadova Yoqut Nurmuxammadjonovna	Gumanitar fanlar va jismoniy tarbiya kafedrasi	O'qituvchi
Tursunov Muxammadyusuf Alisher o'g'li	Ingliz tili va adabiyoti kafedrasi	Kafedra mudiri
A'zamov Sayfulbot Maxamadaliyevich	Ingliz tili va adabiyoti kafedrasi	Bo'lim boshlig'i
Axmadjonov Tursunpo'lat Axmadjon o'g'li	Ingliz tili va adabiyoti kafedrasi	Katta o'qituvchi
Umrzaqov Islomjon Isroilovich	Ingliz tili va adabiyoti kafedrasi	Dotsent
Xujanazarova Nozima Omonjonovna	Ingliz tili va adabiyoti kafedrasi	O'qituvchi-stajer
Madmusayev Jaxongir Muxtorali o'g'li	Ingliz tili va adabiyoti kafedrasi	Katta o'qituvchi
Dadaboyev Olimjon Ortiqovich	Ingliz tili va adabiyoti kafedrasi	Dotsent
Tursunova Moxira Ilxomjonovna	Ingliz tili va adabiyoti kafedrasi	Katta o'qituvchi
Boqiyev Nurali Abdurashid o'g'li	Ingliz tili va adabiyoti kafedrasi	O'qituvchi-stajer
Turg'unova Dilnoza G'ofurjon qizi	Ingliz tili va adabiyoti kafedrasi	Assistent
Nasrullayeva Umida Baxrom qizi	Ingliz tili va adabiyoti kafedrasi	O'qituvchi
Madaminov G'olibjon G'ofurjon o'g'li	Ingliz tili va adabiyoti kafedrasi	O'qituvchi-stajer
Mashrabova Dilnoza Avazxon qizi	Ingliz tili va adabiyoti kafedrasi	O'qituvchi
Ismoilova Zarnigor Raximjon qizi	Ingliz tili va adabiyoti kafedrasi	O'qituvchi-stajer
G'aniyeva Barchinoy Mahmud qizi	Ingliz tili va adabiyoti kafedrasi	O'qituvchi-stajer
Obilov Ibroximjon Vaxobjon o'g'li	Ingliz tili va adabiyoti kafedrasi	O'qituvchi-stajer
Qoraboyev Mirzoxid Xoshimovich	Ingliz tili va adabiyoti kafedrasi	Dotsent
Qodirov Azamat Muxriddinovich	Ingliz tili va adabiyoti kafedrasi	O'qituvchi
Xabibullayev Xakimxo'ja Xamidulla o'g'li	Ingliz tili va adabiyoti kafedrasi	O'qituvchi-stajer
Tursunov Akmaljon Xamidjonovich	Nemis va fransuz tillari kafedrasi	Kafedra mudiri
Tursunov Xusanboy Burgutaliyevich	Nemis va fransuz tillari kafedrasi	Katta o'qituvchi
Madolimov Xusanboy Shuxratovich	Nemis va fransuz tillari kafedrasi	Katta o'qituvchi
Satvoldiyeva Ma'mura Maxammadaminovna	Nemis va fransuz tillari kafedrasi	O'qituvchi
Atamirzayeva E'zoza Bekmirzayevna	Nemis va fransuz tillari kafedrasi	Katta o'qituvchi
Tursunov Zoxidjon Zokirjonovich	Nemis va fransuz tillari kafedrasi	Katta o'qituvchi
Yusupova Umida Inomovna	Nemis va fransuz tillari kafedrasi	Assistent
Mirvaliyev Furqat Shuxratovich	Nemis va fransuz tillari kafedrasi	O'qituvchi-stajer
Raximov Xusniddin Tojakmatovich	Nemis va fransuz tillari kafedrasi	Katta o'qituvchi
Raxmonova Maloxat Abdulxamid qizi	Nemis va fransuz tillari kafedrasi	O'qituvchi
Dodobayev Saminjon Mamajonovich	Nemis va fransuz tillari kafedrasi	Katta o'qituvchi
Abdurasulova Umida Sadullayevna	O'zbek va sharq tillari kafedrasi	Kafedra mudiri
Yandashev Zikirjon Xolmatjon o'g'li	O'zbek va sharq tillari kafedrasi	O'qituvchi-stajer
No'monxonova Muattarxon Nosirxon qizi	O'zbek va sharq tillari kafedrasi	O'qituvchi-stajer
Sobirova Nasiba Avazovna	O'zbek va sharq tillari kafedrasi	O'qituvchi
Xo'janazarova Nazira Omonjonovna	O'zbek va sharq tillari kafedrasi	O'qituvchi
Baqoyev Navro'zjon Abdullo o'g'li	O'zbek va sharq tillari kafedrasi	O'qituvchi-stajer
Erkinov Ahrorbek To'lqinboy o'g'li	O'zbek va sharq tillari kafedrasi	O'qituvchi
Usmonova Soxiba	O'zbek va sharq tillari kafedrasi	O'qituvchi-stajer
Ibragimov Sodiqjon Suyarqul o'g'li	O'zbek va sharq tillari kafedrasi	Assistent
Gafarova Lola Salimbekovna	Rus filologiyasi kafedrasi	Kafedra mudiri
Mirzanazarova Aziza Mirzaabdullayevna	Rus filologiyasi kafedrasi	Katta o'qituvchi
Kazakova Ra'no Mashrabayevna	Rus filologiyasi kafedrasi	Katta o'qituvchi
Kamalova Kadriya Fyodorovna	Rus filologiyasi kafedrasi	Dotsent
Kazakbayeva Saodat Inomiddinovna	Rus filologiyasi kafedrasi	Dotsent
Akmalova Dildora Toxirovna	Rus filologiyasi kafedrasi	Dotsent
Mamadaliyeva Saida Shuxrat qizi	Rus filologiyasi kafedrasi	O'qituvchi
Abdusamatov Mavlonjon Mukarramjon o'g'li	Rus filologiyasi kafedrasi	O'qituvchi
Sobirov Azizbek Baxodir o'g'li	Rus filologiyasi kafedrasi	O'qituvchi-stajer
Mamasodiqova Maxzuna Jalol qizi	Rus filologiyasi kafedrasi	O'qituvchi-stajer
Abdullayeva Iqbola Moxirovna	Rus filologiyasi kafedrasi	Katta o'qituvchi
Yusupova Ra'noxon Kamolhanovna	Rus filologiyasi kafedrasi	Katta o'qituvchi
Yo'ldoshev Muxammad To'lqinboy o'g'li	Rus filologiyasi kafedrasi	O'qituvchi-stajer
Sharofov Javlon Rafiqjon o'g'li	Rus filologiyasi kafedrasi	O'qituvchi-stajer
Mirzakbarova Sevda	Rus filologiyasi kafedrasi	O'qituvchi-stajer
Ermirzayev Abbos Vaxobjonovich	Turizm va tarjima kafedrasi	Kafedra mudiri
Dosbayeva Nargiza Turg'unpo'latovna	Turizm va tarjima kafedrasi	Dotsent
Botirova Palina	Turizm va tarjima kafedrasi	Dotsent
Mirzayev Shavkat Nasibjon o'g'li	Turizm va tarjima kafedrasi	O'qituvchi
Jakbarova Iroda Badriddin qizi	Turizm va tarjima kafedrasi	O'qituvchi-stajer
Xoliqov Zoxidjon Olimjonovich	Turizm va tarjima kafedrasi	Katta o'qituvchi
Tulanboyeva Dildora Tulkinjon qizi	Turizm va tarjima kafedrasi	Katta o'qituvchi
Valijonov Sherzod Abdug'Ani o'g'li	Turizm va tarjima kafedrasi	Katta o'qituvchi
Nematova Maftuna Mirzajon qizi	Turizm va tarjima kafedrasi	Katta o'qituvchi
Salavatova Liliya Enverovna	Turizm va tarjima kafedrasi	O'qituvchi"""

TEXNIK_DATA = """Mamadjonov G'ulomjon Ne'matjonovich	Texnik xodimlar
Nurillajonov Azimjon Rustamjon o'g'li	Texnik xodimlar
Saydullayev Osimxon Nosirxonovich	Texnik xodimlar
Pulatova Surayo Sobitxaonovna	Texnik xodimlar
Yusupova Maxliyoxon Maxammadjanovna	Texnik xodimlar
Nosirova Saodat Odiljonovna	Texnik xodimlar
Madumarova Maxpora Valiyevna	Texnik xodimlar
Tadjibayeva Dilfuza Sobirjonovna	Texnik xodimlar
Inomova Sanobar Isokjoovna	Texnik xodimlar
Qayumova Sadiyaxon Mubillayevna	Texnik xodimlar
Xakimova Xovaxon Kamoljon qizi	Texnik xodimlar
Mamadaliyeva Yoqutxon Samijonovna	Texnik xodimlar
Kamolov Yusupjon Iroilovich	Texnik xodimlar
Ergashev Zuxriddin Ruxitdinovich	Texnik xodimlar
Otaboyeva Roxila Maxamadaliyevna	Texnik xodimlar
Ismatullayev Shukrullo Abdullayevich	Texnik xodimlar
Nuriddinov Tolibjon Qutbiddinovich	Texnik xodimlar
Ergashev Safibullo Sobirovich	Texnik xodimlar
Qoraboyev Baxodir Oripjanovich	Texnik xodimlar
Kosimova Gulbaxor Saypiddinovna	Texnik xodimlar
Jo'rayeva Matlubaxon Maxammadjonovna	Texnik xodimlar
Ibragimova Zebiniso Isroiljonovna	Texnik xodimlar
Abdunazarova Iqbolxon Alijonovna	Texnik xodimlar
Ergasheva Dilrabo	Texnik xodimlar
Odilova Jannatxon Ismoilovna	Texnik xodimlar
Siddiqova Sayyora Saydullo qizi	Texnik xodimlar
Qobilova Shoira Najmiddin qizi	Texnik xodimlar"""

# ── FAKULTET ──────────────────────────────────────────────────────
fak, _ = Fakultet.objects.get_or_create(nomi='Chet tillar')

# ── BO'LIMLAR YARATISH ────────────────────────────────────────────
bolim_nomlari = ['Rahbariyat', 'Mamuriyat', 'Texnik xodimlar']
bolimlar = {}
for nom in bolim_nomlari:
    b, created = Bolim.objects.get_or_create(nomi=nom, defaults={'kerakli_sert': 1})
    bolimlar[nom] = b
    if created:
        print(f"  ✅ Bo'lim yaratildi: {nom}")

# ── KAFEDRALAR YARATISH ───────────────────────────────────────────
kafedra_nomlari = [
    "Ingliz tili o'qitish metodikasi kafedrasi",
    "Gumanitar fanlar va jismoniy tarbiya kafedrasi",
    "Ingliz tili va adabiyoti kafedrasi",
    "Nemis va fransuz tillari kafedrasi",
    "O'zbek va sharq tillari kafedrasi",
    "Rus filologiyasi kafedrasi",
    "Turizm va tarjima kafedrasi",
]
kafedralar = {}
for nom in kafedra_nomlari:
    k, created = Kafedra.objects.get_or_create(nomi=nom, defaults={'fakultet': fak, 'kerakli_sert': 2})
    kafedralar[nom] = k
    if created:
        print(f"  ✅ Kafedra yaratildi: {nom}")

print(f"\n📋 Bo'limlar: {len(bolimlar)} ta, Kafedralar: {len(kafedralar)} ta\n")

# ── XODIMLAR KIRITISH ─────────────────────────────────────────────
xodim_count = 0
for line in (XODIMLAR_DATA + '\n' + TEXNIK_DATA).strip().split('\n'):
    parts = line.split('\t')
    if len(parts) < 2:
        continue
    fio = parts[0].strip()
    bolim_nom = parts[1].strip()
    lavozim = parts[2].strip() if len(parts) > 2 else ''
    if not fio or len(fio) < 3:
        continue
    bolim = bolimlar.get(bolim_nom)
    if bolim and not Xodim.objects.filter(fio__icontains=fio[:15]).exists():
        Xodim.objects.create(fio=fio, bolim=bolim, lavozim=lavozim)
        xodim_count += 1

print(f"✅ Xodimlar kiritildi: {xodim_count} ta")

# ── O'QITUVCHILAR KIRITISH ────────────────────────────────────────
oqit_count = 0
mudirlar = {}  # kafedra: mudiri FIO

for line in OQITUVCHILAR_DATA.strip().split('\n'):
    parts = line.split('\t')
    if len(parts) < 2:
        continue
    fio = parts[0].strip()
    kafedra_nom = parts[1].strip()
    lavozim = parts[2].strip() if len(parts) > 2 else ''
    if not fio or len(fio) < 3:
        continue
    kafedra = kafedralar.get(kafedra_nom)
    if kafedra and not Oqituvchi.objects.filter(fio__icontains=fio[:15]).exists():
        Oqituvchi.objects.create(fio=fio, kafedra=kafedra, lavozim=lavozim)
        oqit_count += 1
        if 'mudiri' in lavozim.lower() or 'kafedra mudiri' in lavozim.lower():
            mudirlar[kafedra_nom] = fio

print(f"✅ O'qituvchilar kiritildi: {oqit_count} ta")

# ── KAFEDRA MUDIRLARI UCHUN USER YARATISH ─────────────────────────
print(f"\n👤 Kafedra mudirlari uchun login yaratilmoqda...\n")

def make_login(fio):
    parts = fio.replace("'","").replace("'","").split()
    if len(parts) >= 2:
        fam = ''.join(c for c in parts[0].lower() if c.isalpha())
        ini = parts[1][0].lower() if parts[1] else ''
        return f"{fam}_{ini}"
    return fio[:10].lower().replace(' ','_')

mudirlar_login = []
for kafedra_nom, fio in mudirlar.items():
    kafedra = kafedralar[kafedra_nom]
    login = make_login(fio)
    base = login
    i = 1
    while User.objects.filter(username=login).exists():
        login = f"{base}{i}"; i += 1

    parts = fio.split()
    u = User.objects.create_user(login, '', 'mudiri123')
    u.last_name = parts[0] if parts else ''
    u.first_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
    u.save()

    pr = UserProfile.objects.create(user=u, rol='kafedra_mudiri', kafedra=kafedra)
    kafedra.mudiri = u
    kafedra.save()

    mudirlar_login.append((fio, login, kafedra_nom))
    print(f"  ✅ {fio[:35]}")
    print(f"     Login: {login} | Parol: mudiri123")
    print(f"     Kafedra: {kafedra_nom}\n")

# ── NATIJA ────────────────────────────────────────────────────────
print("=" * 55)
print("✅ IMPORT YAKUNLANDI!")
print("=" * 55)
print(f"  Bo'limlar      : {Bolim.objects.count()} ta")
print(f"  Kafedralar     : {Kafedra.objects.count()} ta")
print(f"  Xodimlar       : {Xodim.objects.count()} ta")
print(f"  O'qituvchilar  : {Oqituvchi.objects.count()} ta")
print(f"  Kafedra mudirlari: {len(mudirlar_login)} ta")
print()
print("  🔑 KAFEDRA MUDIRLARI PAROLI: mudiri123")
print("=" * 55)

# Loginlar faylga
with open('mudirlar_loginlar.txt', 'w') as f:
    f.write("KAFEDRA MUDIRLARI LOGIN VA PAROLLARI\n")
    f.write("=" * 50 + "\n\n")
    for fio, login, kafedra in mudirlar_login:
        f.write(f"F.I.Sh  : {fio}\n")
        f.write(f"Login   : {login}\n")
        f.write(f"Parol   : mudiri123\n")
        f.write(f"Kafedra : {kafedra}\n")
        f.write("-" * 40 + "\n")

print("\n📄 Loginlar 'mudirlar_loginlar.txt' faylga saqlandi!")
