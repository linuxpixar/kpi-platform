from django.db import models
from django.contrib.auth.models import User

# ── TASHKILIY TUZILMA ─────────────────────────────────────────────

class Fakultet(models.Model):
    nomi = models.CharField("Fakultet nomi", max_length=200, unique=True)
    class Meta: verbose_name="Fakultet"; verbose_name_plural="Fakultetlar"; ordering=['nomi']
    def __str__(self): return self.nomi

class Kafedra(models.Model):
    nomi     = models.CharField("Kafedra nomi", max_length=200)
    fakultet = models.ForeignKey(Fakultet, on_delete=models.CASCADE, related_name='kafedralar')
    mudiri   = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='mudirlik_kafedra', verbose_name="Kafedra mudiri")
    kerakli_sert = models.PositiveIntegerField("Kerakli sertifikat soni (o'qituvchi)", default=2)
    class Meta: verbose_name="Kafedra"; verbose_name_plural="Kafedralar"; ordering=['nomi']
    def __str__(self): return f"{self.nomi} ({self.fakultet.nomi})"

class Bolim(models.Model):
    nomi     = models.CharField("Bo'lim nomi", max_length=200)
    boshlig  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='boshqaruv_bolim', verbose_name="Bo'lim boshlig'i")
    kerakli_sert = models.PositiveIntegerField("Kerakli sertifikat soni (xodim)", default=2)
    class Meta: verbose_name="Bo'lim"; verbose_name_plural="Bo'limlar"; ordering=['nomi']
    def __str__(self): return self.nomi

class Guruh(models.Model):
    nomi     = models.CharField("Guruh nomi", max_length=100)
    fakultet = models.ForeignKey(Fakultet, on_delete=models.CASCADE, related_name='guruhlar')
    kurs     = models.PositiveSmallIntegerField("Kurs", default=1)
    tyutor   = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='tyutor_guruhlar', verbose_name="Tyutor")
    kerakli_sert = models.PositiveIntegerField("Kerakli sertifikat soni (talaba)", default=1)
    class Meta: verbose_name="Guruh"; verbose_name_plural="Guruhlar"; ordering=['nomi']
    def __str__(self): return self.nomi

# ── SHAXSLAR ──────────────────────────────────────────────────────

class Talaba(models.Model):
    fio    = models.CharField("To'liq F.I.O.", max_length=200)
    guruh  = models.ForeignKey(Guruh, on_delete=models.CASCADE, related_name='talabalar')
    class Meta: verbose_name="Talaba"; verbose_name_plural="Talabalar"; ordering=['fio']
    def __str__(self): return f"{self.fio} ({self.guruh.nomi})"

    def sertifikat_soni(self):
        return self.sertifikatlar.count()

    def kpi_foiz(self):
        kerak = self.guruh.kerakli_sert
        if not kerak: return 100
        return min(int(self.sertifikat_soni() / kerak * 100), 100)

class Xodim(models.Model):
    fio    = models.CharField("To'liq F.I.O.", max_length=200)
    bolim  = models.ForeignKey(Bolim, on_delete=models.CASCADE, related_name='xodimlar')
    lavozim = models.CharField("Lavozim", max_length=200, blank=True)
    class Meta: verbose_name="Xodim"; verbose_name_plural="Xodimlar"; ordering=['fio']
    def __str__(self): return f"{self.fio} ({self.bolim.nomi})"

    def sertifikat_soni(self):
        return self.sertifikatlar.count()

    def kpi_foiz(self):
        kerak = self.bolim.kerakli_sert
        if not kerak: return 100
        return min(int(self.sertifikat_soni() / kerak * 100), 100)

class Oqituvchi(models.Model):
    fio     = models.CharField("To'liq F.I.O.", max_length=200)
    kafedra = models.ForeignKey(Kafedra, on_delete=models.CASCADE, related_name='oqituvchilar')
    lavozim = models.CharField("Lavozim", max_length=200, blank=True)
    class Meta: verbose_name="O'qituvchi"; verbose_name_plural="O'qituvchilar"; ordering=['fio']
    def __str__(self): return f"{self.fio} ({self.kafedra.nomi})"

    def sertifikat_soni(self):
        return self.sertifikatlar.count()

    def kpi_foiz(self):
        kerak = self.kafedra.kerakli_sert
        if not kerak: return 100
        return min(int(self.sertifikat_soni() / kerak * 100), 100)

# ── SERTIFIKAT ────────────────────────────────────────────────────

class Sertifikat(models.Model):
    talaba    = models.ForeignKey(Talaba,    on_delete=models.CASCADE, null=True, blank=True, related_name='sertifikatlar')
    xodim     = models.ForeignKey(Xodim,     on_delete=models.CASCADE, null=True, blank=True, related_name='sertifikatlar')
    oqituvchi = models.ForeignKey(Oqituvchi, on_delete=models.CASCADE, null=True, blank=True, related_name='sertifikatlar')

    nomi       = models.CharField("Sertifikat nomi", max_length=300)
    tashkilot  = models.CharField("Bergan tashkilot", max_length=200, blank=True)
    link       = models.URLField("Sertifikat linki", max_length=500)
    berilgan   = models.DateField("Berilgan sana", null=True, blank=True)
    yuklagan   = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='yuklagan_sertlar')
    yaratilgan = models.DateTimeField(auto_now_add=True)

    class Meta: verbose_name="Sertifikat"; verbose_name_plural="Sertifikatlar"; ordering=['-yaratilgan']

    def __str__(self):
        egasi = self.talaba or self.xodim or self.oqituvchi
        return f"{egasi} — {self.nomi}"

    def egasi_fio(self):
        if self.talaba: return self.talaba.fio
        if self.xodim: return self.xodim.fio
        if self.oqituvchi: return self.oqituvchi.fio
        return "—"

    def egasi_tur(self):
        if self.talaba: return "Talaba"
        if self.xodim: return "Xodim"
        if self.oqituvchi: return "O'qituvchi"
        return "—"

    def egasi_bolim(self):
        if self.talaba: return self.talaba.guruh.nomi
        if self.xodim: return self.xodim.bolim.nomi
        if self.oqituvchi: return self.oqituvchi.kafedra.nomi
        return "—"

# ── USER PROFIL ───────────────────────────────────────────────────

ROL_CHOICES = [
    ('tyutor',          'Tyutor'),
    ('bolim_boshlig',   "Bo'lim boshlig'i"),
    ('kafedra_mudiri',  'Kafedra mudiri'),
]

class UserProfile(models.Model):
    user    = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    rol = models.CharField("Rol", max_length=30, choices=ROL_CHOICES, default='tyutor')
    guruhlar = models.ManyToManyField(Guruh, blank=True, verbose_name="Guruhlar (tyutor uchun)", related_name="tyutorlar")
    bolim   = models.ForeignKey(Bolim,    on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Bo'lim (boshlig' uchun)")
    kafedra = models.ForeignKey(Kafedra,  on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Kafedra (mudiri uchun)")
    class Meta: verbose_name="Foydalanuvchi profili"; verbose_name_plural="Foydalanuvchi profillari"
    def __str__(self): return f"{self.user.get_full_name() or self.user.username} ({self.get_rol_display()})"
