import math
import time
import random

# ==========================================
# 1. COUCHE LOGIQUE & MATHÉMATIQUE (CORE)
# ==========================================
class FormuleFuturiste:
    def __init__(self):
        # Pondérations initiales (Surface, Deep, Darknet)
        self.alpha = [0.5, 0.3, 0.2]
        # Métriques de base simulées [Surface, Deep, Darknet]
        self.securite_base = [0.95, 0.95, 0.90]
        self.fiabilite_base = [0.99, 0.90, 0.80]
        
        # Facteurs technologiques émergents
        self.Q = 1.1       # Facteur Quantique (Optimise la sécurité)
        self.B = 1.05      # Facteur Blockchain (Consensus / Immuabilité)
        self.C_t = 1.2     # Facteur Cognitif initial (IA adaptative)

    def calculer_puissance_futuriste(self, alert_level=0):
        # Ajustement dynamique par l'IA cognitive en cas d'alerte réseau
        if alert_level > 0:
            self.C_t = min(1.5, self.C_t + 0.1)  # L'IA s'amplifie
            self.alpha[2] = min(0.4, self.alpha[2] + 0.05) # On donne du poids au Darknet résilient
        else:
            self.C_t = max(1.2, self.C_t - 0.05)

        total_p = 0
        for i in range(3):
            # Application de la formule : (S^Q * F^B * C)
            S_futur = math.pow(self.securite_base[i], self.Q)
            F_futur = math.pow(self.fiabilite_base[i], self.B)
            
            total_p += self.alpha[i] * (S_futur * F_futur * self.C_t)
        
        # Normalisation académique pour la projection (moyenne pondérée globale)
        return min(1.0, total_p / 3.0)

# ==========================================
# 2. COUCHE INFRASTRUCTURE SIMULÉE (NODES)
# ==========================================
class ReseauUnifie:
    def __init__(self):
        self.formule = FormuleFuturiste()
        self.noeuds = {
            "Surface": {"status": "ONLINE", "traffic": 100},
            "Deep": {"status": "ONLINE", "traffic": 50},
            "Darknet": {"status": "ONLINE", "traffic": 10}
        }

    def simuler_evenement(self):
        # Simulation d'une attaque ou surcharge aléatoire sur le réseau
        evenement = random.choice(["RAS", "ATTAQUE_SURFACE", "SURCHARGE_DARKNET"])
        alert = 0
        
        if evenement == "ATTAQUE_SURFACE":
            print("\n[!] Alerte : Attaque par déni de service sur la couche Surface.")
            self.noeuds["Surface"]["traffic"] += 200
            self.formule.securite_base[0] = max(0.5, self.formule.securite_base[0] - 0.15)
            alert = 1
        elif evenement == "SURCHARGE_DARKNET":
            print("\n[!] Alerte : Flux massif de routage anonyme détecté sur le Darknet.")
            self.noeuds["Darknet"]["traffic"] += 80
            self.formule.fiabilite_base[2] = max(0.4, self.formule.fiabilite_base[2] - 0.2)
            alert = 2
        else:
            print("\n[*] Flux réseau stable. Régulation nominale.")
            # Récupération progressive
            self.formule.securite_base = [0.95, 0.95, 0.90]
            self.formule.fiabilite_base = [0.99, 0.90, 0.80]
            
        return alert

    def executer_cycles(self, nb_cycles=5):
        for cycle in range(1, nb_cycles + 1):
            print(f"\n=== CYCLE DE SIMULATION {cycle} ===")
            alerte = self.simuler_evenement()
            
            # Calcul de la puissance globale via le moteur mathématique
            p_globale = self.formule.calculer_puissance_futuriste(alert_level=alerte)
            
            print(f"-> Métrique adaptative IA (C_t) : {self.formule.C_t:.2f}")
            print(f"-> Probabilité de résilience du Pont (Pr_futur) : {p_globale * 100:.2f}%")
            time.sleep(1)

if __name__ == "__main__":
    print("Initialisation du Pont Évolutif Universel...")
    reseau = ReseauUnifie()
    reseau.executer_cycles(5)
