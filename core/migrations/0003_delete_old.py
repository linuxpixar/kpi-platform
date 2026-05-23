from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [('core','0002_alter_sertifikat_tur_alter_sertifikat_yuklagan_and_more')]
    operations = [
        migrations.DeleteModel(name='UserProfile'),
    ]
