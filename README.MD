# Application de Liste de Tâches

Cette application est une simple liste de tâches écrite en Python. Elle permet aux utilisateurs d'ajouter, de visualiser, de mettre à jour, de supprimer et de marquer des tâches comme complétées. Les tâches sont sauvegardées dans un fichier JSON pour une persistance des données.

## Fonctionnalités

- **Ajouter une tâche** : Ajoutez une nouvelle tâche avec un titre, une description, une priorité et une date d'échéance.
- **Voir toutes les tâches** : Affichez toutes les tâches avec leurs détails, y compris le nombre de jours restants jusqu'à la date d'échéance.
- **Mettre à jour une tâche** : Modifiez les détails d'une tâche existante.
- **Supprimer une tâche** : Supprimez une tâche de la liste.
- **Compléter une tâche** : Marquez une tâche comme complétée.

## Prérequis

- Python 3.x
- Module `json` (inclus par défaut avec Python)
- Module `os` (inclus par défaut avec Python)
- Module `datetime` (inclus par défaut avec Python)

## Installation

1. Clonez ce dépôt ou téléchargez les fichiers source.
2. Assurez-vous que Python 3.x est installé sur votre machine.

## Utilisation

1. Exécutez le script Python :

   ```bash
   python TO DO LIST.py
   ```

2. Suivez les instructions affichées dans le terminal pour interagir avec l'application.

## Structure du Code

- **`load_tasks()`** : Charge les tâches depuis un fichier JSON.
- **`save_tasks()`** : Sauvegarde les tâches dans un fichier JSON.
- **`display_menu()`** : Affiche le menu principal de l'application.
- **`add_task()`** : Ajoute une nouvelle tâche.
- **`view_tasks()`** : Affiche toutes les tâches.
- **`update_task()`** : Met à jour une tâche existante.
- **`delete_task()`** : Supprime une tâche.
- **`complete_task()`** : Marque une tâche comme complétée.
- **`main()`** : Point d'entrée de l'application.

## Contribution

Les contributions sont les bienvenues! Veuillez soumettre une pull request ou ouvrir une issue pour discuter des changements que vous souhaitez apporter.

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.