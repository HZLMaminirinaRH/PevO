import http.server
import socket
import subprocess
import math
import sys
import time
import json

class OrchestrateurCognitif:
    """
    Orchestrateur Cognitif - Applique la formule P(t) = Σ αᵢ · Sᵢ(t) · Fᵢ(t)
    Coordonne les trois couches (Surface, Deep, Darknet) selon leurs rôles spécialisés.
    """

    def __init__(self):
        # Coefficients de pondération par couche (Surface, Deep, Darknet)
        self.alpha = [0.4, 0.35, 0.25]

        # Sécurité dynamique pour chaque couche
        self.S = [0.95, 0.85, 0.70]

        # Fiabilité progressive de base
        self.F_base = [0.99, 0.90, 0.60]

        # Facteur cognitif (ajustement IA en temps réel)
        self.C_t = 1.0

        # Chemins des binaires
        self.bin_rust = "./nodes/darknet_node/target/release/darknet_node"
        self.bin_go = "./nodes/deep_node/deep_node"

    def appliquer_xor(self, donnees_str):
        return bytes([b ^ 0x42 for b in donnees_str.encode('utf-8')])

    def dechiffrer_xor(self, donnees_bytes):
        return "".join([chr(b ^ 0x42) for b in donnees_bytes])

    def calculer_fiabilite_deep(self, F_base):
        """Interroge le nœud Go pour la fiabilité progressive (couche Deep)"""
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(2.0)
            client.connect(("127.0.0.1", 8082))

            requete = f"{F_base},1.05,Deep"
            client.send(self.appliquer_xor(requete))

            reponse_chiffree = client.recv(1024)
            client.close()
            return float(self.dechiffrer_xor(reponse_chiffree).strip())
        except Exception:
            return F_base

    def calculer_securite_darknet(self):
        """Interroge le nœud Rust pour la sécurité bas niveau (couche Darknet)"""
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(2.0)
            client.connect(("127.0.0.1", 8081))

            requete = f"5.0,0.25,0.70,1.35"
            client.send(self.appliquer_xor(requete))

            reponse_chiffree = client.recv(1024)
            client.close()
            return float(self.dechiffrer_xor(reponse_chiffree).strip())
        except Exception:
            return self.S[2]

    def calculer_pont_probability(self):
        """
        Calcule P(t) = Σ αᵢ · Sᵢ(t) · Fᵢ(t)
        P(t) = α₁·S₁(t)·F₁(t) + α₂·S₂(t)·F₂(t) + α₃·S₃(t)·F₃(t)
        """
        # Couche 1: Surface (calcul local)
        F1 = self.F_base[0]
        P1 = self.alpha[0] * self.S[0] * F1 * self.C_t

        # Couche 2: Deep (depuis nœud Go)
        F2 = self.calculer_fiabilite_deep(self.F_base[1])
        P2 = self.alpha[1] * self.S[1] * F2 * self.C_t

        # Couche 3: Darknet (depuis nœud Rust)
        S3 = self.calculer_securite_darknet()
        F3 = self.F_base[2]
        P3 = self.alpha[2] * S3 * F3 * self.C_t

        P_total = min(1.0, P1 + P2 + P3)

        return {
            "P_surface": P1,
            "P_deep": P2,
            "P_darknet": P3,
            "P_total": P_total,
            "C_t": self.C_t,
            "alpha": self.alpha
        }

    def optimiser_ia_cognitive(self, perturbations=False):
        """Ajuste les paramètres en réponse aux perturbations"""
        if perturbations:
            print("[IA] Perturbation détectée ! Adaptation en cours...")
            self.C_t = 1.45
            self.alpha = [0.2, 0.35, 0.45]
        else:
            print("[IA] Réseau en état nominal.")
            self.C_t = 1.0
            self.alpha = [0.4, 0.35, 0.25]


class HandlerHebergement(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            try:
                with open("www/index.html", "rb") as fichier:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(fichier.read())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Erreur critique : Fichier index.html introuvable.")
        else:
            super().do_GET()


if __name__ == "__main__":
    print("=== PevO : Orchestrateur Cognitif Polyglotte ===")
    moteur = OrchestrateurCognitif()

    serveur_port = 8080
    serveur_http = http.server.HTTPServer(("0.0.0.0", serveur_port), HandlerHebergement)
    print(f"[Python] Orchestrateur actif sur http://localhost:{serveur_port}")

    try:
        moteur.optimiser_ia_cognitive(perturbations=False)
        results = moteur.calculer_pont_probability()
        print(f"[PevO] P(t) = {results['P_total']:.4f}")
        serveur_http.serve_forever()
    except KeyboardInterrupt:
        print("\n[PevO] Fermeture de l'orchestrateur.")
        serveur_http.server_close()
        sys.exit(0)
