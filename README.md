# Sertifikat Yuklash Platformasi — NDCTI

## O'rnatish va ishga tushirish

### 1. Python va pip borligini tekshiring
```bash
python --version   # 3.8+ bo'lishi kerak
pip --version
```

### 2. Django o'rnatish
```bash
pip install django
```

### 3. Ma'lumotlar bazasini yaratish
```bash
python manage.py migrate
```

### 4. Admin foydalanuvchi yaratish
```bash
python manage.py createsuperuser
# yoki tayyor: admin/admin123 allaqachon bor
```

### 5. Serverni ishga tushirish
```bash
python manage.py runserver
# http://127.0.0.1:8000 da ochiladi
```

---

## Foydalanuvchilar (demo)

| Login    | Parol    | Huquq         |
|----------|----------|---------------|
| admin    | admin123 | Admin (barcha imkoniyat) |
| user     | user123  | Oddiy foydalanuvchi |

---

## Sahifalar

| URL              | Tavsif                          |
|------------------|---------------------------------|
| `/`              | Login sahifasi                  |
| `/bosh/`         | Bosh sahifa (dashboard)         |
| `/yuklash/`      | Sertifikat yuklash formasi      |
| `/mening/`       | Mening sertifikatlarim          |
| `/admin-panel/`  | Barcha sertifikatlar (admin)    |
| `/statistika/`   | Statistika (admin)              |
| `/django-admin/` | Django admin paneli             |

---

## CSV eksport

Admin panel → "CSV yuklash" tugmasini bosing.
Filter qo'llanilgan holda ham eksport ishlaydi.

---

## Production uchun

`settings.py` da quyidagilarni o'zgartiring:
- `DEBUG = False`
- `SECRET_KEY` ni yangi, xavfsiz kalit bilan almashtiring
- `ALLOWED_HOSTS` ga domeningizni qo'shing

---

**Mas'ul:** Sh.Usmonov — Raqamli ta'lim texnologiyalari markazi direktori  
**Asos:** 2-A/O-sonli buyruq · 8-band · 10.2-kichik band
