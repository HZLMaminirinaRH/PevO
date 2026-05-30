import http.server
import socket
import subprocess
import math
import sys
import time
import json

from core.security_matrix import (
    MatriceSecuriteEvolutive,
    NiveauMenace,
    COUCHE_SURFACE, COUCHE_DEEP, COUCHE_DARKNET, COUCHE_AGENTIQUE,
)

class OrchestrateurCognitif:
    """
    Orchestrateur Cognitif - Applique la formule P(t) = Σ αᵢ · Sᵢ(t) · Fᵢ(t) · C_t

    Coordonne désormais QUATRE couches :
      0. Surface    (Python)  — web classique, point d'entrée HTTP
      1. Deep       (Go)      — fiabilité progressive + consensus blockchain
      2. Darknet    (Rust)    — sécurité bas niveau, décroissance dynamique
      3. Agentique  (IA)      — 4ᵉ couche émergente : substrat des agents
                                cognitifs. Son S/F est piloté par C_t.

    La sécurité n'est plus un booléen : la MatriceSecuriteEvolutive mesure
    en temps réel le niveau de menace par couche (DDoS, SQLi, XSS…) et
    module directement Sᵢ(t), C_t et les poids αᵢ.
    """

    def __init__(self):
        # Coefficients de pondération nominaux (Surface, Deep, Darknet, Agentique)
        self.alpha_nominal = [0.35, 0.30, 0.20, 0.15]
        self.alpha = list(self.alpha_nominal)

        # Sécurité dynamique de base pour chaque couche
        self.S = [0.95, 0.85, 0.70, 0.80]

        # Fiabilité progressive de base
        self.F_base = [0.99, 0.90, 0.60, 0.75]

        # Facteur cognitif (ajustement IA en temps réel)
        self.C_t = 1.0

        # Matrice de sécurité évolutive : cœur défensif branché sur la formule
        self.matrice = MatriceSecuriteEvolutive()

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

    def calculer_securite_agentique(self):
        """
        Sécurité de la 4ᵉ couche (Agentique). N'ayant pas de nœud dédié,
        elle dérive du facteur cognitif : un C_t élevé signifie une IA en
        posture défensive active, donc une couche agentique plus vigilante.
        S₄(t) = base · (0.7 + 0.3·C_t), bornée à [0,1].
        """
        s4 = self.S[3] * (0.7 + 0.3 * self.C_t)
        return max(0.0, min(1.0, s4))

    def calculer_pont_probability(self):
        """
        Calcule P(t) = Σ αᵢ · Sᵢ(t) · Fᵢ(t) · C_t  sur les 4 couches.

        Chaque sécurité Sᵢ(t) est MODULÉE par la matrice de sécurité :
        si une couche subit une attaque (SQLi/XSS/DDoS), son facteur chute
        et son poids αᵢ est redistribué vers les couches saines.
        """
        # Facteurs de sécurité temps réel issus de la matrice (∈ ]0,1])
        fs = [self.matrice.facteur_securite_couche(c)
              for c in (COUCHE_SURFACE, COUCHE_DEEP, COUCHE_DARKNET, COUCHE_AGENTIQUE)]

        # Couche 1: Surface (calcul local)
        F1 = self.F_base[0]
        P1 = self.alpha[0] * (self.S[0] * fs[0]) * F1 * self.C_t

        # Couche 2: Deep (depuis nœud Go)
        F2 = self.calculer_fiabilite_deep(self.F_base[1])
        P2 = self.alpha[1] * (self.S[1] * fs[1]) * F2 * self.C_t

        # Couche 3: Darknet (depuis nœud Rust)
        S3 = self.calculer_securite_darknet()
        F3 = self.F_base[2]
        P3 = self.alpha[2] * (S3 * fs[2]) * F3 * self.C_t

        # Couche 4: Agentique (locale, pilotée par l'IA)
        S4 = self.calculer_securite_agentique()
        F4 = self.F_base[3]
        P4 = self.alpha[3] * (S4 * fs[3]) * F4 * self.C_t

        P_total = min(1.0, P1 + P2 + P3 + P4)

        return {
            "P_surface": P1,
            "P_deep": P2,
            "P_darknet": P3,
            "P_agentique": P4,
            "P_total": P_total,
            "C_t": self.C_t,
            "alpha": self.alpha,
            "menace_globale": self.matrice.niveau_menace_global().name,
        }

    def optimiser_ia_cognitive(self, perturbations=None):
        """
        Ajuste les paramètres en réponse aux MENACES RÉELLES mesurées par la
        matrice de sécurité (et non plus un simple booléen).

        - C_t est tiré de la posture défensive recommandée par la matrice.
        - Les poids αᵢ sont redistribués : on retire du poids aux couches
          attaquées pour le donner aux couches saines (résilience du pont).

        `perturbations` (legacy) reste accepté : True force le mode critique,
        False force le mode nominal — utile pour les tests et simulations.
        """
        # Compatibilité ascendante : override manuel éventuel
        if perturbations is True:
            self.matrice.menace_par_couche[COUCHE_DARKNET] = NiveauMenace.CRITIQUE
        elif perturbations is False:
            for c in self.matrice.menace_par_couche:
                self.matrice.menace_par_couche[c] = NiveauMenace.NOMINAL

        niveau = self.matrice.niveau_menace_global()

        # Le facteur cognitif suit la menace : l'IA accélère son adaptation
        self.C_t = self.matrice.facteur_cognitif_recommande()

        # Redistribution adaptative des poids autour des couches saines
        self.alpha = self.matrice.ponderation_adaptative(self.alpha_nominal)

        if niveau >= NiveauMenace.ELEVE:
            print(f"[IA] ⚠️  Menace {niveau.name} détectée ! "
                  f"Adaptation C_t={self.C_t:.2f}, α={[round(a,3) for a in self.alpha]}")
        elif niveau == NiveauMenace.SURVEILLANCE:
            print(f"[IA] 👁️  Surveillance accrue. C_t={self.C_t:.2f}")
        else:
            print("[IA] ✅ Réseau en état nominal.")

        return niveau


class HandlerHebergement(http.server.SimpleHTTPRequestHandler):
    """
    Point d'entrée HTTP de la couche Surface, durci par la matrice de
    sécurité. Chaque requête passe par : rate limiting → analyse
    d'injection → en-têtes durcis. Toute attaque détectée fait monter le
    niveau de menace, ce qui reconfigure la formule P(t) en temps réel.
    """

    # Instance partagée injectée depuis le bloc principal
    orchestrateur = None

    def _ip_client(self):
        # Respecte un éventuel proxy de confiance, sinon IP directe
        return self.headers.get("X-Forwarded-For", self.client_address[0]).split(",")[0].strip()

    def _envoyer_entetes_securite(self):
        for cle, valeur in self.orchestrateur.matrice.entetes_securite().items():
            self.send_header(cle, valeur)
        self._entetes_envoyes = True  # empêche le doublon dans end_headers()

    def _refuser(self, code, message):
        self.send_response(code)
        self._envoyer_entetes_securite()
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(message.encode("utf-8"))

    def do_GET(self):
        matrice = self.orchestrateur.matrice
        ip = self._ip_client()

        # ── Couche 1 : rate limiting / anti-DDoS ─────────────────────────
        autorisee, raison = matrice.autoriser_requete(ip)
        if not autorisee:
            self.orchestrateur.optimiser_ia_cognitive()  # réaction immédiate
            self._refuser(429, f"Trop de requêtes ({raison}). Réessayez plus tard.")
            return

        # ── Couche 2 : détection d'injection sur l'URL ───────────────────
        verdict = matrice.analyser_charge_utile(self.path, COUCHE_SURFACE)
        if not verdict["sure"]:
            self.orchestrateur.optimiser_ia_cognitive()  # menace → reconfig P(t)
            self._refuser(403, f"Requête bloquée : {', '.join(verdict['menaces'])}")
            return

        # ── Service du contenu (avec en-têtes durcis) ────────────────────
        if self.path == "/" or self.path == "/index.html":
            try:
                with open("www/index.html", "rb") as fichier:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self._envoyer_entetes_securite()
                    self.end_headers()
                    self.wfile.write(fichier.read())
            except Exception:
                self._refuser(500, "Erreur critique : index.html introuvable.")
        else:
            super().do_GET()

    def end_headers(self):
        # Filet de sécurité : garantir les en-têtes durcis sur les réponses
        # servies par la classe parente (fichiers statiques).
        if self.orchestrateur is not None and not getattr(self, "_entetes_envoyes", False):
            for cle, valeur in self.orchestrateur.matrice.entetes_securite().items():
                self.send_header(cle, valeur)
            self._entetes_envoyes = True
        super().end_headers()

    def log_message(self, format, *args):
        # Journalisation silencieuse (évite de divulguer la stack en clair)
        pass


if __name__ == "__main__":
    print("=== PevO : Orchestrateur Cognitif Polyglotte ===")
    moteur = OrchestrateurCognitif()

    # Injection de l'orchestrateur dans le handler (matrice partagée)
    HandlerHebergement.orchestrateur = moteur

    serveur_port = 8080
    serveur_http = http.server.HTTPServer(("0.0.0.0", serveur_port), HandlerHebergement)
    print(f"[Python] Orchestrateur actif sur http://localhost:{serveur_port}")
    print(f"[🛡️] Matrice de sécurité évolutive branchée sur P(t) — 4 couches actives.")

    try:
        moteur.optimiser_ia_cognitive()
        results = moteur.calculer_pont_probability()
        print(f"[PevO] P(t) = {results['P_total']:.4f} | Menace : {results['menace_globale']}")
        print(f"[PevO] Couches → Surface={results['P_surface']:.3f} "
              f"Deep={results['P_deep']:.3f} Darknet={results['P_darknet']:.3f} "
              f"Agentique={results['P_agentique']:.3f}")
        serveur_http.serve_forever()
    except KeyboardInterrupt:
        print("\n[PevO] Fermeture de l'orchestrateur.")
        serveur_http.server_close()
        sys.exit(0)
