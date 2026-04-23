from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audiences', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='audience',
            name='decision',
            field=models.CharField(blank=True, choices=[('gagnee', 'Gagnée'), ('perdue', 'Perdue')], default='', max_length=20),
        ),
    ]
