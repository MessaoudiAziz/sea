import json
import os
import threading
import time

class Contact:
    """Classe représentant un contact."""
    def __init__(self, nom, telephone):
        self.nom = nom
        self.telephone = telephone

    def to_dict(self):
        """Convertit le contact en dictionnaire pour JSON."""
        return {"nom": self.nom, "telephone": self.telephone}

class GestionnaireDeContacts:
    """Classe pour gérer les contacts."""
    def __init__(self, fichier='contacts.json'):
        self.contacts = []
        self.fichier = fichier
        self.semaphore = threading.Semaphore(1)  # Permet à un thread à la fois d'accéder aux données
        self.charger_contacts()

    def ajouter_contact(self, nom, telephone):
        """Ajoute un nouveau contact."""
        with self.semaphore:  # Accès synchronisé
            contact = Contact(nom, telephone)
            self.contacts.append(contact)
            self.sauvegarder_contacts()
        return f"Contact '{nom}' ajouté avec succès."

    def lister_contacts(self):
        """Retourne tous les contacts."""
        with self.semaphore:
            if not self.contacts:
                return "Aucun contact trouvé."
            return [{"nom": contact.nom, "telephone": contact.telephone} for contact in self.contacts]

    def rechercher_contact(self, nom):
        """Recherche un contact par son nom."""
        with self.semaphore:
            for contact in self.contacts:
                if contact.nom.lower() == nom.lower():
                    return {"nom": contact.nom, "telephone": contact.telephone}
            return f"Aucun contact trouvé avec le nom '{nom}'."

    def sauvegarder_contacts(self):
        """Sauvegarde les contacts dans un fichier JSON."""
        with open(self.fichier, 'w') as f:
            json.dump([contact.to_dict() for contact in self.contacts], f)

    def charger_contacts(self):
        """Charge les contacts depuis un fichier JSON."""
        if os.path.exists(self.fichier):
            with open(self.fichier, 'r') as f:
                contacts_data = json.load(f)
                self.contacts = [Contact(**data) for data in contacts_data]

def mesurer_temps_execution(fonction):
    """Décorateur pour mesurer le temps d'exécution d'une fonction."""
    def wrapper(*args, **kwargs):
        debut = time.time()
        resultat = fonction(*args, **kwargs)
        fin = time.time()
        print(f"Temps d'exécution : {fin - debut:.4f} secondes")
        return resultat
    return wrapper

def afficher_menu():
    """Affiche le menu principal."""
    print("\nMenu :")
    print("1. Ajouter un contact")
    print("2. Lister les contacts")
    print("3. Rechercher un contact")
    print("4. Quitter")

@mesurer_temps_execution
def executer_commande(gestionnaire, commande, *args):
    """Exécute une commande dans un thread."""
    thread = threading.Thread(target=commande, args=args)
    thread.start()
    thread.join()

def main():
    """Fonction principale."""
    gestionnaire = GestionnaireDeContacts()

    while True:
        afficher_menu()
        choix = input("Choisissez une option : ")

        if choix == '1':
            nom = input("Entrez le nom du contact : ")
            telephone = input("Entrez le numéro de téléphone : ")
            executer_commande(gestionnaire, gestionnaire.ajouter_contact, nom, telephone)
        elif choix == '2':
            def lister():
                contacts = gestionnaire.lister_contacts()
                if isinstance(contacts, list):
                    print(f"{'Nom':<20} {'Téléphone':<15}")
                    print("-" * 35)
                    for contact in contacts:
                        print(f"{contact['nom']:<20} {contact['telephone']:<15}")
                else:
                    print(contacts)
            executer_commande(gestionnaire, lister)
        elif choix == '3':
            nom = input("Entrez le nom du contact à rechercher : ")
            def rechercher():
                result = gestionnaire.rechercher_contact(nom)
                if isinstance(result, dict):
                    print(f"Contact trouvé - Nom: {result['nom']}, Téléphone: {result['telephone']}")
                else:
                    print(result)
            executer_commande(gestionnaire, rechercher)
        elif choix == '4':
            print("Au revoir!")
            break
        else:
            print("Choix invalide, veuillez réessayer.")

if __name__ == "__main__":
    main()
