import http.server
import urllib.request
import socket
import subprocess
import math
import sys
import time
import random

class MoteurPolyglotte:
    def __init__(self):
        # Coefficients initiaux : l'équilibrage standard du Pont
        self.alpha = [0.5, 0.3, 0.2]
        # ... (le reste de votre __init__ actuel) ...

    def appliquer_xor(self, donnees_str):
        # 8 espaces d'indentation ici
        return bytes([b ^ 0x42 for b in donnees_str.encode('utf-8')])

    def dechiffrer_xor(self, donnees_bytes):
        # 8 espaces d'indentation ici
        return "".join([chr(b ^ 0x42) for b in donnees_bytes])

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
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(2.0)
            client.connect(("127.0.0.1", 8081))
            
            # Encapsulation chiffrée de la requête
            requete = f"{self.t},{self.lambda_dark},{self.beta_dark},{self.Q}"
            client.send(self.appliquer_xor(requete))
            
            # Décapsulage chiffré de la réponse
            reponse_chiffree = client.recv(1024)
            client.close()
            return float(self.dechiffrer_xor(reponse_chiffree).strip())
        except Exception:
            return 0.85

    def exécuter_calcul_go(self, fiab_base, b_factor, nom_couche):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(2.0)
            client.connect(("127.0.0.1", 8082))
            
            # Encapsulation chiffrée de la requête
            requete = f"{fiab_base},{b_factor},{nom_couche}"
            client.send(self.appliquer_xor(requete))
            
            # Décapsulage chiffrée de la réponse
            reponse_chiffree = client.recv(1024)
            client.close()
            return float(self.dechiffrer_xor(reponse_chiffree).strip())
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

class HandlerHebergement(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Si l'utilisateur demande la racine, on va chercher la page hébergée chez le nœud Go
        try:
            with urllib.request.urlopen("http://127.0.0.1:8083/") as reponse:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(reponse.read())
        except Exception:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Erreur de liaison avec le noeud de stockage Go.")

if __name__ == "__main__":
    print("=== PevO : Lancement de l'Infrastructure avec Hébergement Web ===")
    moteur = MoteurPolyglotte()
    
    # Lancement du serveur Web public sur le port 8080 (Accessible sur votre réseau)
    serveur_port = 80
    serveur_http = http.server.HTTPServer(("0.0.0.0", serveur_port), HandlerHebergement)
    print(f"[Python] Serveur d'hébergement public ouvert sur http://localhost:{serveur_port}")
    
    try:
        # On effectue un cycle initial de calcul pour armer l'IA
        moteur.optimiser_ia_cognitive(perturbations=False)
        moteur.calculer_resilience_globale()
        
        # Le script reste en écoute pour distribuer le site web gratuitement
        serveur_http.serve_forever()
    except KeyboardInterrupt:
        print("\n[PevO] Fermeture de l'hébergement.")
        serveur_http.server_close()
        sys.exit(0)
