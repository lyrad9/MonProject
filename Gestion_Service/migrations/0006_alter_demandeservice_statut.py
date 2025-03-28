# Generated by Django 5.1.4 on 2025-03-24 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gestion_Service', '0005_remove_demandeservice_montant_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demandeservice',
            name='statut',
            field=models.CharField(choices=[('EN_ATTENTE', 'En attente'), ('VALIDÉE', 'Validée'), ('REFUSÉE', 'Refusée')], default='EN_ATTENTE', max_length=12),
        ),
    ]
