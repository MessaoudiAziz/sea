import json
import os
from multiprocessing import Process, Pipe

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
        self.charger_contacts()

    def ajouter_contact(self, nom, telephone):
        """Ajoute un nouveau contact."""
        contact = Contact(nom, telephone)
        self.contacts.append(contact)
        self.sauvegarder_contacts()
        return f"Contact '{nom}' ajouté avec succès."

    def lister_contacts(self):
        """Retourne tous les contacts."""
        if not self.contacts:
            return "Aucun contact trouvé."
        return [{"nom": contact.nom, "telephone": contact.telephone} for contact in self.contacts]

    def rechercher_contact(self, nom):
        """Recherche un contact par son nom."""
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

def processus_gestionnaire(pipe_conn):
    """Processus secondaire pour gérer les contacts."""
    gestionnaire = GestionnaireDeContacts()
    while True:
        try:
            message = pipe_conn.recv()
            commande = message.get("commande")
            if commande == "ajouter":
                result = gestionnaire.ajouter_contact(message["nom"], message["telephone"])
            elif commande == "lister":
                result = gestionnaire.lister_contacts()
            elif commande == "rechercher":
                result = gestionnaire.rechercher_contact(message["nom"])
            elif commande == "quitter":
                result = "Processus de gestion des contacts terminé."
                pipe_conn.send(result)
                break
            else:
                result = "Commande inconnue."
            pipe_conn.send(result)
        except EOFError:
            # Arrêt propre si le Pipe est fermé par le processus principal
            break

def afficher_menu():
    """Affiche le menu principal."""
    print("\nMenu :")
    print("1. Ajouter un contact")
    print("2. Lister les contacts")
    print("3. Rechercher un contact")
    print("4. Quitter")

def main():
    """Fonction principale."""
    parent_conn, child_conn = Pipe()
    gestionnaire_process = Process(target=processus_gestionnaire, args=(child_conn,))
    gestionnaire_process.start()

    try:
        while True:
            afficher_menu()
            choix = input("Choisissez une option : ")

            if choix == '1':
                nom = input("Entrez le nom du contact : ")
                telephone = input("Entrez le numéro de téléphone : ")
                parent_conn.send({"commande": "ajouter", "nom": nom, "telephone": telephone})
                print(parent_conn.recv())
            elif choix == '2':
                parent_conn.send({"commande": "lister"})
                contacts = parent_conn.recv()
                if isinstance(contacts, list):
                    print(f"{'Nom':<20} {'Téléphone':<15}")
                    print("-" * 35)
                    for contact in contacts:
                        print(f"{contact['nom']:<20} {contact['telephone']:<15}")
                else:
                    print(contacts)
            elif choix == '3':
                nom = input("Entrez le nom du contact à rechercher : ")
                parent_conn.send({"commande": "rechercher", "nom": nom})
                result = parent_conn.recv()
                if isinstance(result, dict):
                    print(f"Contact trouvé - Nom: {result['nom']}, Téléphone: {result['telephone']}")
                else:
                    print(result)
            elif choix == '4':
                parent_conn.send({"commande": "quitter"})
                print(parent_conn.recv())
                break
            else:
                print("Choix invalide, veuillez réessayer.")
    except KeyboardInterrupt:
        print("\nArrêt du programme par l'utilisateur.")
        parent_conn.send({"commande": "quitter"})  # Assurez la fermeture propre du processus enfant
    finally:
        gestionnaire_process.join()

if __name__ == "__main__":
    main()

