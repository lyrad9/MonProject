# Analyse du Projet de Gestion de Services

## Description Générale

Ce projet est une application web développée avec Django pour la gestion de services et de demandes client. L'application permet aux utilisateurs de consulter des services, faire des demandes, recevoir des devis et gérer des factures.

## Structure du Projet

### Technologies Utilisées

- **Framework Backend**: Django 5.1.4
- **Base de Données**: MySQL
- **Bibliothèques principales**:
  - `mysqlclient`: Pour la connexion à MySQL
  - `pillow`: Pour la gestion des images
  - `weasyprint`: Pour la génération de PDF
  - `PyMySQL`: Driver alternatif pour MySQL

### Organisation des Dossiers

```
MonProject/
├── AppGestionService/       # Application principale (configuration Django)
├── Gestion_Service/         # Application pour la gestion des services
├── utilisateurs/            # Application pour la gestion des utilisateurs
├── templates/               # Templates HTML de l'application
├── static/                  # Fichiers statiques (CSS, JS, images)
├── media/                   # Contenu uploadé par les utilisateurs
├── manage.py                # Script de gestion Django
└── requirements.txt         # Dépendances du projet
```

## Schéma de la Base de Données

### Modèle Utilisateur

```
User (utilisateurs/models.py)
├── username [CharField]     # Hérité de AbstractUser
├── password [CharField]     # Hérité de AbstractUser
├── email [EmailField]       # Hérité de AbstractUser
├── first_name [CharField]   # Hérité de AbstractUser
├── last_name [CharField]    # Hérité de AbstractUser
├── adresse [TextField]      # Adresse du client (facultatif)
└── entreprise [CharField]   # Nom de l'entreprise (facultatif)
```

### Modèles de Gestion de Services

```
Categorie (Gestion_Service/models.py)
├── nom [CharField]          # Nom de la catégorie
├── description [TextField]  # Description de la catégorie
└── date_creation [DateField]# Date de création (auto)

Service (Gestion_Service/models.py)
├── nom [CharField]          # Nom du service
├── description [TextField]  # Description du service
├── image [ImageField]       # Image du service (facultatif)
├── date_creation [DateField]# Date de création (auto)
└── categorie [ForeignKey]   # Relation avec Categorie (plusieurs services par catégorie)

DemandeService (Gestion_Service/models.py)
├── description [TextField]              # Description de la demande
├── date_creation [DateTimeField]        # Date de création (auto)
├── date_modification [DateTimeField]    # Date de dernière modification (auto)
├── montant [DecimalField]               # Montant associé à la demande
├── service [ForeignKey]                 # Relation avec Service
├── client [ForeignKey]                  # Relation avec User
├── fichier [FileField]                  # Fichier associé (facultatif)
└── statut [CharField]                   # Statut (EN_ATTENTE, VALIDÉ, REFUSÉ)

Devis (Gestion_Service/models.py)
├── demande [OneToOneField]              # Relation avec DemandeService
├── fichier [FileField]                  # Fichier du devis (facultatif)
├── date_creation [DateTimeField]        # Date de création (auto)
└── statut [CharField]                   # Statut (EN_ATTENTE, VALIDÉ, REFUSÉ)

Facture (Gestion_Service/models.py)
├── description [TextField]              # Description de la facture
├── date_creation [DateField]            # Date de création (auto)
├── date_modification [DateTimeField]    # Date de dernière modification (auto)
├── montant [DecimalField]               # Montant de la facture
├── taxe [DecimalField]                  # TVA (facultatif)
├── devis [OneToOneField]                # Relation avec Devis
├── statut [CharField]                   # Statut (PAYEE, IMPAYEE)
├── invoice_type [CharField]             # Type (RECEIPT, PROFORMA, INVOICE)
├── fichier_pdf [FileField]              # Fichier PDF de la facture
├── mode_paiement [CharField]            # Mode de paiement (CB, VIREMENT, CHEQUE)
└── numero_facture [CharField]           # Numéro unique de facture
```

## Relations entre les Modèles

- Un **utilisateur (User)** peut faire plusieurs **demandes de service (DemandeService)**
- Une **catégorie (Categorie)** contient plusieurs **services (Service)**
- Un **service (Service)** peut avoir plusieurs **demandes (DemandeService)**
- Une **demande (DemandeService)** peut avoir un seul **devis (Devis)**
- Un **devis (Devis)** peut avoir une seule **facture (Facture)**

## Fonctionnalités Principales

### Gestion des Utilisateurs

- Inscription et connexion des utilisateurs
- Profils utilisateurs avec adresse et entreprise
- Système de permissions et rôles (un utilisateur peut être soit Administrateur, soit Employé ou Client)

### Gestion des Services

- Catalogue de services organisé par catégories
- Page détaillée pour chaque service avec description et image

### Gestion des Demandes

- Création de demandes de service par les clients
- Suivi du statut des demandes
- Possibilité de joindre des fichiers aux demandes

### Gestion des Devis et Factures

- Génération de devis pour les demandes de service
- Acceptation ou refus des devis par les clients
- Génération automatique de factures au format PDF
- Suivi du statut des paiements

## Configuration Technique

### Base de Données

- MySQL avec configuration InnoDB
- Connexion via mysqlclient et PyMySQL

### Email

- Configuration SMTP pour les notifications par email
- Templates d'email HTML personnalisés

### Fichiers Statiques et Media

- Gestion des fichiers uploadés dans le dossier media/
- Organisation des fichiers statiques pour le développement et la production

### Sécurité

- Protection CSRF activée
- Validation des mots de passe
- Système d'authentification personnalisé
