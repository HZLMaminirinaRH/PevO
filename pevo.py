import socket
import subprocess
import math
import sys
import random

class MoteurPolyglotte:
    def __init__(self):
        # Coefficients initiaux : l'équilibrage standard du Pont
        self.alpha = [0.5, 0.3, 0.2] 
        
        # Métriques de base (S_i et F_i)
        self.securite_base = [0.95, 0.95, 0.70]
        self.fiabilite_base = [0.99, 0.90, 0.60]
        
        # Variables temporelles et technologiques
        self.t = 5.0          
        self.lambda_dark = 0.25 
        self.beta_dark = 0.70  
        
        self.Q = 1.35         # Facteur Quantique
        self.B = 1.05         # Facteur Blockchain
        self.C_t = 1.0        # Facteur Cognitif (Départ nominal)

        self.bin_rust = "./nodes/darknet_node/target/release/darknet_node"
        self.bin_go = "./nodes/deep_node/deep_node"

    def exécuter_calcul_rust(self):
        try:
            # Création d'une socket client TCP
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(2.0) # Évite les blocages infinis
            client.connect(("127.0.0.1", 8081))
            
            # Formatage de la chaîne de paramètres : "t,lambda,beta,Q"
            requete = f"{self.t},{self.lambda_dark},{self.beta_dark},{self.Q}"
            client.send(requete.encode('utf-8'))
            
            # Récupération de la réponse du serveur Rust
            reponse = client.recv(1024).decode('utf-8')
            client.close()
            return float(reponse.strip())
        except Exception as e:
            # En cas d'absence du serveur Rust (pas encore lancé), repli mathématique local
            lambda_eff = self.lambda_dark / self.Q
            s_i_t = math.exp(-lambda_eff * self.t) + self.beta_dark
            return min(1.0, math.pow(s_i_t, self.Q))

    def exécuter_calcul_go(self, fiab_base, b_factor, nom_couche):
        try:
            res = subprocess.run([self.bin_go, str(fiab_base), str(b_factor), nom_couche], 
                                 capture_output=True, text=True, check=True)
            return float(res.stdout.strip())
        except Exception:
            return 0.90

    def optimiser_ia_cognitive(self, perturbations=False):
        """
        MATÉRIALISATION DU FACTEUR COGNITIF C(t) :
        L'IA analyse les performances en temps réel. En cas de perturbation sur une couche,
        elle augmente sa puissance de calcul C(t) et réorganise les poids alpha_i 
        pour favoriser le vecteur le plus sûr.
        """
        if perturbations:
            print("[IA] Perturbation détectée ! Activation de la boucle d'optimisation...")
            self.C_t = 1.45  # L'IA s'amplifie (surcroît cognitif)
            
            # Réallocation dynamique des poids alpha (Somme toujours égale à 1.0)
            # Le Darknet quantique et le Deep Web décentralisé deviennent prioritaires
            self.alpha = [0.1, 0.4, 0.5]
        else:
            print("[IA] État du réseau nominal. Régulation stable.")
            self.C_t = 1.15
            self.alpha = [0.5, 0.3, 0.2]

    def calculer_resilience_globale(self):
        # Couche Surface
        S0_f = math.pow(self.securite_base[0], self.Q)
        F0_f = math.pow(self.fiabilite_base[0], self.B)
        P0 = self.alpha[0] * (S0_f * F0_f * self.C_t)

        # Couche Deep (Via binaire Go)
        S1_f = math.pow(self.securite_base[1], self.Q)
        F1_f = self.exécuter_calcul_go(self.fiabilite_base[1], self.B, "Deep_Web")
        P1 = self.alpha[1] * (S1_f * F1_f * self.C_t)

        # Couche Darknet (Via binaire Rust)
        S2_f = self.exécuter_calcul_rust()
        F2_f = math.pow(self.fiabilite_base[2], self.B)
        P2 = self.alpha[2] * (S2_f * F2_f * self.C_t)

        return min(1.0, P0 + P1 + P2)

if __name__ == "__main__":
    print("=== PevO : Simulation du Moteur Cognitif Adaptatif ===")
    moteur = MoteurPolyglotte()
    
    # Étape A : Simulation en mode Nominal
    moteur.optimiser_ia_cognitive(perturbations=False)
    p_nominal = moteur.calculer_resilience_globale()
    print(f"-> Résilience en mode Nominal : {p_nominal * 100:.2f}%")
    print(f"-> Distribution des charges (alpha) : {moteur.alpha}\n")
    
    # Étape B : Simulation en mode Crise / Attaque
    moteur.optimiser_ia_cognitive(perturbations=True)
    p_crise = moteur.calculer_resilience_globale()
    print(f"-> Résilience sous Optimisation IA : {p_crise * 100:.2f}%")
    print(f"-> Nouvelle distribution adaptative (alpha) : {moteur.alpha}")
    
    sys.exit(0)
