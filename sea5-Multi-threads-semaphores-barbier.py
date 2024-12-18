import threading
import queue
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
    def __init__(self):
        self.contacts = []

    def ajouter_contact(self, nom, telephone):
        """Ajoute un nouveau contact."""
        time.sleep(1)  # Simulation d'un traitement
        contact = Contact(nom, telephone)
        self.contacts.append(contact)
        print(f"[Barbier] Contact '{nom}' ajouté avec succès.")

    def lister_contacts(self):
        """Retourne tous les contacts."""
        time.sleep(1)  # Simulation d'un traitement
        if not self.contacts:
            print("[Barbier] Aucun contact trouvé.")
        else:
            print("[Barbier] Liste des contacts :")
            for contact in self.contacts:
                print(f"  - Nom: {contact.nom}, Téléphone: {contact.telephone}")

    def rechercher_contact(self, nom):
        """Recherche un contact par son nom."""
        time.sleep(1)  # Simulation d'un traitement
        for contact in self.contacts:
            if contact.nom.lower() == nom.lower():
                print(f"[Barbier] Contact trouvé : Nom: {contact.nom}, Téléphone: {contact.telephone}")
                return
        print(f"[Barbier] Aucun contact trouvé avec le nom '{nom}'.")

class Barbier:
    """Classe représentant le barbier."""
    def __init__(self, gestionnaire, capacite_salle_attente=5):
        self.gestionnaire = gestionnaire
        self.queue = queue.Queue(capacite_salle_attente)
        self.running = True

    def traiter_demandes(self):
        """Traitement des demandes par le barbier."""
        while self.running or not self.queue.empty():
            try:
                # Récupérer une tâche de la file (bloque si vide)
                demande, args = self.queue.get(timeout=1)
                print("[Barbier] Une tâche est en cours de traitement...")
                demande(*args)
                self.queue.task_done()
            except queue.Empty:
                print("[Barbier] La file d'attente est vide, le barbier attend...")

    def ajouter_demande(self, demande, *args):
        """Ajoute une demande à la file d'attente."""
        try:
            self.queue.put((demande, args), timeout=1)
            print("[Client] Une nouvelle demande a été ajoutée à la file.")
        except queue.Full:
            print("[Client] La file est pleine, le client repart.")

    def arreter(self):
        """Arrête le barbier."""
        self.running = False

def afficher_menu():
    """Affiche le menu principal."""
    print("\nMenu :")
    print("1. Ajouter un contact")
    print("2. Lister les contacts")
    print("3. Rechercher un contact")
    print("4. Quitter")

def main():
    """Fonction principale."""
    gestionnaire = GestionnaireDeContacts()
    barbier = Barbier(gestionnaire)

    # Démarrage du thread du barbier
    thread_barbier = threading.Thread(target=barbier.traiter_demandes)
    thread_barbier.start()

    try:
        while True:
            afficher_menu()
            choix = input("Choisissez une option : ")

            if choix == '1':
                nom = input("Entrez le nom du contact : ")
                telephone = input("Entrez le numéro de téléphone : ")
                barbier.ajouter_demande(gestionnaire.ajouter_contact, nom, telephone)
            elif choix == '2':
                barbier.ajouter_demande(gestionnaire.lister_contacts)
            elif choix == '3':
                nom = input("Entrez le nom du contact à rechercher : ")
                barbier.ajouter_demande(gestionnaire.rechercher_contact, nom)
            elif choix == '4':
                print("Au revoir!")
                break
            else:
                print("Choix invalide, veuillez réessayer.")
    finally:
        barbier.arreter()
        thread_barbier.join()

if __name__ == "__main__":
    main()
