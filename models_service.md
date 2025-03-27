# Analyse Détaillée des Modèles - Gestion_Service

## Vue d'ensemble

Cette documentation analyse les modèles de données de l'application de gestion de services. L'application permet de gérer des catégories de services, des services, des demandes de service, des devis et des factures.

## Modèle Catégorie

Le modèle `Categorie` représente les différentes catégories de services proposés.

### Attributs

- **nom** : Chaîne de caractères (max 255 caractères) - Le nom de la catégorie
- **description** : Texte - La description détaillée de la catégorie (valeur par défaut : chaîne vide)
- **date_creation** : Date - Date de création de la catégorie (ajoutée automatiquement)

### Meta

- **ordering** : [`-date_creation`] - Tri par date de création décroissante (plus récent d'abord)

### Méthodes

- \***\*str**()\*\* : Retourne le nom de la catégorie comme représentation textuelle

## Modèle Service

Le modèle `Service` représente les services spécifiques proposés dans l'application.

### Attributs

- **nom** : Chaîne de caractères (max 255 caractères) - Le nom du service
- **description** : Texte - La description détaillée du service (optionnel)
- **image** : Image - Image associée au service (optionnel)
- **date_creation** : Date - Date de création du service (mise à jour automatiquement)
- **categorie** : Clé étrangère vers `Categorie` - La catégorie à laquelle appartient le service

### Relations

- Un service appartient à une seule catégorie
- Une catégorie peut contenir plusieurs services (relation one-to-many)

### Meta

- **ordering** : [`-date_creation`] - Tri par date de création décroissante
- **verbose_name** : "Service"
- **verbose_name_plural** : "Services"

### Méthodes

- \***\*str**()\*\* : Retourne le nom du service
- **get_absolute_url()** : Retourne l'URL 'home' pour la redirection après création/modification

## Modèle DemandeService

Le modèle `DemandeService` représente les demandes de service faites par les clients.

### Attributs

- **description** : Texte - Description détaillée de la demande
- **date_creation** : DateTime - Date et heure de création de la demande (ajoutée automatiquement)
- **date_modification** : DateTime - Date et heure de dernière modification (mise à jour automatiquement)
- **montant** : Décimal - Montant associé à la demande (10 chiffres avec 2 décimales, défaut : 0)
- **service** : Clé étrangère vers `Service` - Le service demandé
- **client** : Clé étrangère vers `User` - L'utilisateur qui fait la demande
- **fichier** : Fichier - Document associé à la demande (optionnel)
- **statut** : Chaîne de caractères - Statut de la demande (choix : 'EN_ATTENTE', 'VALIDÉ', 'REFUSÉ', défaut : 'EN_ATTENTE')

### Relations

- Une demande concerne un seul service
- Un service peut être associé à plusieurs demandes
- Une demande est faite par un seul client
- Un client peut faire plusieurs demandes

### Meta

- **ordering** : [`-date_creation`] - Tri par date de création décroissante
- **verbose_name** : "DemandeService"
- **verbose_name_plural** : "DemandeServices"

### Méthodes

- \***\*str**()\*\* : Retourne une chaîne formatée avec l'ID et le statut de la demande

## Modèle Devis

Le modèle `Devis` représente les devis générés pour les demandes de service.

### Attributs

- **demande** : OneToOneField vers `DemandeService` - La demande de service concernée
- **fichier** : Fichier - Le fichier du devis (optionnel)
- **date_creation** : DateTime - Date et heure de création du devis (ajoutée automatiquement)
- **statut** : Chaîne de caractères - Statut du devis (choix : 'EN_ATTENTE', 'VALIDÉ', 'REFUSÉ', défaut : 'EN_ATTENTE')

### Relations

- Un devis est associé à une seule demande (one-to-one)
- Une demande ne peut avoir qu'un seul devis

### Meta

- **ordering** : [`-date_creation`] - Tri par date de création décroissante
- **verbose_name** : "Devis"
- **verbose_name_plural** : "Devis"

### Méthodes

- \***\*str**()\*\* : Retourne une chaîne formatée avec l'ID du devis et le nom d'utilisateur du client

## Modèle Facture

Le modèle `Facture` représente les factures générées à partir des devis acceptés.

### Attributs

- **description** : Texte - Description détaillée de la facture (optionnel, max 1000 caractères)
- **date_creation** : Date - Date de création de la facture (ajoutée automatiquement)
- **date_modification** : DateTime - Date et heure de dernière modification (mise à jour automatiquement)
- **montant** : Décimal - Montant de la facture (10 chiffres avec 2 décimales, défaut : 0)
- **taxe** : Décimal - Pourcentage de taxe appliqué (5 chiffres avec 2 décimales, optionnel)
- **devis** : OneToOneField vers `Devis` - Le devis associé à cette facture (optionnel)
- **statut** : Chaîne de caractères - Statut du paiement (choix : 'PAYEE', 'IMPAYEE', défaut : 'IMPAYEE')
- **invoice_type** : Chaîne de caractères - Type de facture (choix : 'RECEIPT', 'PROFORMA INVOICE', 'INVOICE')
- **fichier_pdf** : Fichier - Le fichier PDF de la facture (généré automatiquement, optionnel)
- **mode_paiement** : Chaîne de caractères - Mode de paiement (choix : 'CB', 'VIREMENT', 'CHEQUE', défaut : 'CB')
- **numero_facture** : Chaîne de caractères - Numéro unique de la facture (généré automatiquement, format 'FAC-XXXXXX')

### Relations

- Une facture est associée à un seul devis (one-to-one)
- Un devis ne peut avoir qu'une seule facture

### Meta

- **ordering** : [`-date_creation`] - Tri par date de création décroissante
- **verbose_name** : "Facture"
- **verbose_name_plural** : "Factures"

### Méthodes

- **save()** : Méthode surchargée pour générer automatiquement le numéro de facture et calculer le total TTC
- \***\*str**()\*\* : Retourne une chaîne formatée avec le numéro de facture et le montant
- **get_client()** : Retourne le client associé à cette facture via la relation avec le devis
- **get_service()** : Retourne le service associé à cette facture via la relation avec le devis
- **generate_pdf()** : Génère un fichier PDF pour la facture en utilisant un template HTML et le stocke dans l'attribut fichier_pdf

## Relations entre les modèles

1. **Catégorie → Service** : Une catégorie peut contenir plusieurs services (one-to-many)
2. **Service → DemandeService** : Un service peut être demandé plusieurs fois (one-to-many)
3. **User → DemandeService** : Un utilisateur peut faire plusieurs demandes (one-to-many)
4. **DemandeService → Devis** : Une demande peut avoir un seul devis (one-to-one)
5. **Devis → Facture** : Un devis peut avoir une seule facture (one-to-one)

## Flux de travail typique

1. Un utilisateur sélectionne un service d'une catégorie
2. L'utilisateur crée une demande de service
3. La demande est traitée et un devis est généré
4. Si le devis est accepté, une facture est générée
5. La facture peut être payée via différents modes de paiement
