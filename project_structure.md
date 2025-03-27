Ce projet est une application web Django avec plusieurs modules.

## Fichiers racine

- manage.py - Script Django pour gérer l'application
- Pipfile - Fichier de configuration pour pip
- Pipfile.lock - Fichier de configuration pour pip
- Procfile - Fichier de configuration pour Heroku
- requirements.txt - Fichier de configuration pour pip
- settings.py - Paramètres du projet Django
- urls.py - Configuration des URL principales
- wsgi.py - Interface pour serveurs web

## Fichiers de configuration

- Plusieurs fichiers de documentation (README.md, settings.md, models_service.md, permissions.md)
- Fichiers de log (**django_debug.log**, **django_email_debug.log**)
- Fichiers de configuration de la base de données (info.py)
- Fichiers de configuration de l'application (settings.py)
- Dossier de base de données (db)
- Dossier de migrations (migrations)
- Dossier de médias (media)
- Dossier de fichiers statiques (static)
- Dossier de fichiers JavaScript (static/js)
- Dossier de fichiers CSS (static/css)

## Structure du projet

Applications principales

### AppGestionService - Configuration principale du projet Django

- settings.py - Paramètres du projet Django
- urls.py - Configuration des URL principales
- asgi.py et wsgi.py - Interfaces pour serveurs web
- info.py - Informations sur l'application

### Gestion_Service - Application principale

- models.py - Modèles de données (195 lignes)
- views.py - Vues et logique métier (437 lignes)
- urls.py - Routes de l'application
- admin.py - Configuration de l'interface d'administration
- signals.py - Gestion des signaux Django
- Dossier migrations - Migrations de base de données

### utilisateurs - Gestion des utilisateurs

- models.py - Modèles des utilisateurs
- views.py - Vues liées aux utilisateurs (220 lignes)
- urls.py - Routes pour la gestion des utilisateurs
- token.py - Gestion des tokens d'authentification
- admin.py - Administration des utilisateurs

### Structure frontend

- media - Dossier pour les fichiers média (images uploadées, etc.)
- static - Ressources statiques
- templates - Fichiers HTML
- base.html - Template de base (484 lignes)
  **Sous-dossiers organisés par fonctionnalité:**
- auth/ - Templates d'authentification
- devis/ - Templates pour les devis
- home/ - Templates de la page d'accueil
- services/ - Templates des services
- users/ - Templates de gestion utilisateurs
- Autres templates spécifiques (login, register, devis, facture)
- css/ - Fichiers de style
- javaScripts/ - Fichiers JavaScript

  **Technologies utilisées**
  Backend: Django 5.1.4
  Base de données: MySQL (via mysqlclient et PyMySQL)
  Génération PDF: WeasyPrint
  Traitement d'images: Pillow
  Ce projet semble être une application de gestion de services avec fonctionnalités de facturation, authentification utilisateur et gestion des permissions.
