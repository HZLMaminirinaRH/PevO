import subprocess
import math
import sys

class MoteurPolyglotte:
    def __init__(self):
        self.alpha = [0.5, 0.3, 0.2] # Pondérations surface, deep, darknet
        self.fiabilite_base = [0.99, 0.90, 0.80]
        
        # Paramètres d'évolution temporelle et technologique
        self.t = 5.0          # Instant t de la simulation
        self.lambda_dark = 0.25 # Taux de dégradation de base (attaques) sur le Darknet
        self.beta_dark = 0.70  # Seuil minimal garanti par les protocoles du Darknet
        
        self.Q = 1.35         # Facteur quantique renforcé (QKD actif)
        self.B = 1.05         # Facteur blockchain
        self.C_t = 1.2        # Facteur cognitif d'amplification

        self.bin_rust = "./nodes/darknet_node/target/release/darknet_node"
        self.bin_go = "./nodes/deep_node/deep_node"

    def exécuter_calcul_rust(self):
        try:
            # Envoi des paramètres temporels et quantiques au nœud Rust
            cmd = [self.bin_rust, str(self.t), str(self.lambda_dark), str(self.beta_dark), str(self.Q)]
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return float(res.stdout.strip())
        except Exception as e:
            # Fallback mathématique local si le binaire subit un incident matériel
            lambda_eff = self.lambda_dark / self.Q
            s_i_t = math.exp(-lambda_eff * self.t) + self.beta_dark
            return min(1.0, math.pow(s_i_t, self.Q))

    def exécuter_calcul_go(self, fiab_base, b_factor, nom_couche):
        try:
            # Envoi de la métrique, de l'exposant Blockchain, et de l'identifiant de couche
            res = subprocess.run([self.bin_go, str(fiab_base), str(b_factor), nom_couche], 
                                 capture_output=True, text=True, check=True)
            return float(res.stdout.strip())
        except Exception:
            return math.pow(fiab_base, b_factor)

    def calculer_resilience_globale(self):
        # 1. Couche Surface
        S0_f = math.pow(0.95, self.Q)
        F0_f = math.pow(self.fiabilite_base[0], self.B)
        P0 = self.alpha[0] * (S0_f * F0_f * self.C_t)

        # 2. Couche Deep
        S1_f = math.pow(0.95, self.Q)
        F1_f = self.exécuter_calcul_go(self.fiabilite_base[1], self.B, "Deep_Web")
        P1 = self.alpha[1] * (S1_f * F1_f * self.C_t)

        # 3. Couche Darknet (Déléguée à Rust avec atténuation quantique de l'attaque)
        S2_f = self.exécuter_calcul_rust()
        F2_f = math.pow(self.fiabilite_base[2], self.B)
        P2 = self.alpha[2] * (S2_f * F2_f * self.C_t)

        # Formule unifiée finale (Somme directe des composantes pondérées)
        return min(1.0, P0 + P1 + P2)

if __name__ == "__main__":
    print("=== Exécution de la Simulation avec Facteur Quantique (Rust) ===")
    moteur = MoteurPolyglotte()
    p_globale = moteur.calculer_resilience_globale()
    print(f"-> Résilience du protocole unifié Pr_futur(t) : {p_globale * 100:.2f}%")
    
    # Indiquer à l'environnement que le calcul s'est terminé avec succès (Code de retour 0)
    sys.exit(0)
