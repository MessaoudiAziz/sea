import json  
import os  

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

    def lister_contacts(self):  
        """Liste tous les contacts."""  
        if not self.contacts:  
            print("Aucun contact trouvé.")  
            return  
        for contact in self.contacts:  
            print(f"Nom: {contact.nom}, Téléphone: {contact.telephone}")  

    def rechercher_contact(self, nom):  
        """Recherche un contact par son nom."""  
        for contact in self.contacts:  
            if contact.nom.lower() == nom.lower():  
                print(f"Contact trouvé - Nom: {contact.nom}, Téléphone: {contact.telephone}")  
                return  
        print(f"Aucun contact trouvé avec le nom '{nom}'.")  

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

def afficher_menu():  
    """Affiche le menu principal."""  
    print("\nMenu :")  
    print("1. Ajouter un contact")  
    print("2. Lister les contacts")  
    print("3. Rechercher un contact")  
    print("4. Quitter")  

def main():  
    """Fonction principale du programme."""  
    gestionnaire = GestionnaireDeContacts()  

    while True:  
        afficher_menu()  
        choix = input("Choisissez une option : ")  

        if choix == '1':  
            nom = input("Entrez le nom du contact : ")  
            telephone = input("Entrez le numéro de téléphone : ")  
            gestionnaire.ajouter_contact(nom, telephone)  
            print(f"Contact '{nom}' ajouté avec succès.")  
        elif choix == '2':  
            gestionnaire.lister_contacts()  
        elif choix == '3':  
            nom_a_rechercher = input("Entrez le nom du contact à rechercher : ")  
            gestionnaire.rechercher_contact(nom_a_rechercher)  
        elif choix == '4':  
            print("Au revoir!")  
            break  
        else:  
            print("Choix invalide, veuillez réessayer.")  

if __name__ == "__main__":  
    main()
