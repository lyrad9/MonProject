# Explication du fichier settings.py

Ce document explique en détail la configuration du projet Django dans le fichier `settings.py`.

## Configuration générale

- **BASE_DIR** : Chemin de base du projet Django, utilisé pour construire d'autres chemins relatifs.
- **SECRET_KEY** : Clé secrète utilisée pour la sécurité, il est recommandé de ne pas la partager en production.
- **DEBUG** : Réglé sur `True`, ce qui active le mode débogage. Il devrait être désactivé en production.

## Applications installées

Le projet contient les applications suivantes :

- Applications Django par défaut (admin, auth, contenttypes, sessions, messages, staticfiles)
- `utilisateurs` : Application personnalisée pour la gestion des utilisateurs
- `Gestion_Service` : Application personnalisée pour la gestion de services

## Configuration de la base de données

Le projet utilise MySQL avec les paramètres suivants:

- Nom de la base de données : `app_bd`
- Utilisateur : `root`
- Mot de passe : vide
- Hôte : `localhost`
- Port : `3306`
- Configuration pour utiliser InnoDB comme moteur de stockage par défaut

## Configuration des emails

- Utilisation de `django.core.mail.backends.smtp.EmailBackend`
- Configuration SMTP avec TLS
- Les informations sensibles (hôte, utilisateur, mot de passe, port) sont importées depuis un fichier `info.py`
- Email administrateur : `edjabeadam1@gmail.com`

## Authentification et sécurité

- **LOGIN_URL** : `login` - URL pour rediriger les utilisateurs non authentifiés
- **LOGIN_REDIRECT_URL** : `home` - URL après connexion réussie
- **LOGOUT_REDIRECT_URL** : `login` - URL après déconnexion
- **AUTH_USER_MODEL** : `utilisateurs.User` - Modèle utilisateur personnalisé
- Validateurs de mot de passe standards configurés

## Fichiers statiques et médias

- **STATIC_URL** : `static/` - Préfixe d'URL pour les fichiers statiques
- **STATICFILES_DIRS** : Liste des répertoires où Django cherche les fichiers statiques
- **STATIC_ROOT** : `staticfiles/` - Répertoire où les fichiers statiques sont collectés pour le déploiement
- **MEDIA_URL** : `/media/` - Préfixe d'URL pour les fichiers média uploadés
- **MEDIA_ROOT** : Chemin absolu où les fichiers média sont stockés

## Middlewares

Configuration standard des middlewares Django, incluant :

- Sécurité
- Sessions
- CSRF (protection contre les attaques Cross-Site Request Forgery)
- Authentification
- Messages
- Protection contre le clickjacking

## Templates

Les templates sont configurés pour être recherchés dans le dossier `templates` à la racine du projet, ainsi que dans les applications installées.

## Internationalisation

- **LANGUAGE_CODE** : `en-us` - Langue par défaut
- **TIME_ZONE** : `UTC` - Fuseau horaire
- **USE_I18N** : `True` - Activation de l'internationalisation
- **USE_TZ** : `True` - Activation des fuseaux horaires

## Journalisation (Logging)

Configuration d'un système de journalisation pour déboguer les problèmes d'envoi d'emails, avec les logs écrits dans le fichier `django_email_debug.log`.

## Remarques de sécurité

- **CSRF_COOKIE_HTTPONLY** est désactivé
- En mode production, il faudrait :
  - Désactiver `DEBUG`
  - Changer la `SECRET_KEY`
  - Configurer correctement `ALLOWED_HOSTS`
  - Revoir les paramètres de sécurité
