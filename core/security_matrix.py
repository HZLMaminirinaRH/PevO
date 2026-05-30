"""
Matrice de Sécurité Évolutive de PevO
=====================================
Implémente les défenses concrètes (DDoS/Megalodon, SQLi, XSS, CSRF, abus d'API)
et les traduit en signaux qui pilotent la formule cognitive :

    P(t) = Σ αᵢ · Sᵢ(t) · Fᵢ(t) · C_t

Au lieu d'un booléen `perturbations`, l'orchestrateur reçoit ici un
NIVEAU DE MENACE mesuré en temps réel par couche. Ce niveau abaisse la
sécurité dynamique Sᵢ(t) de la couche attaquée et augmente le facteur
cognitif C_t (réflexe d'adaptation de l'IA).

Aucune dépendance externe : tout fonctionne avec la stdlib + cryptography
(déjà utilisée par ipfs_security.py).
"""

import re
import time
import hmac
import hashlib
import secrets
from collections import defaultdict, deque
from datetime import datetime
from enum import IntEnum


class NiveauMenace(IntEnum):
    """Niveaux de menace, du plus calme au plus critique."""
    NOMINAL = 0      # Réseau sain
    SURVEILLANCE = 1 # Anomalies mineures
    ELEVE = 2        # Attaque probable en cours
    CRITIQUE = 3     # Attaque confirmée (DDoS massif, exploitation active)


# Couches de PevO (index alignés sur la formule P(t))
COUCHE_SURFACE = 0
COUCHE_DEEP = 1
COUCHE_DARKNET = 2
COUCHE_AGENTIQUE = 3  # 4ᵉ couche émergente (Web Agentique / Cognitif)

NOMS_COUCHES = {
    COUCHE_SURFACE: "Surface",
    COUCHE_DEEP: "Deep",
    COUCHE_DARKNET: "Darknet",
    COUCHE_AGENTIQUE: "Agentique",
}


class MatriceSecuriteEvolutive:
    """
    Cœur défensif de PevO. Analyse chaque requête entrante, calcule un
    niveau de menace par couche, et expose des facteurs de modulation
    consommés directement par l'OrchestrateurCognitif.
    """

    # ── Signatures d'attaques (détection par motifs) ──────────────────────
    # Injection SQL : mots-clés et tautologies classiques + blind SQLi
    _MOTIFS_SQLI = [
        re.compile(r"(?i)\bunion\b.{1,40}\bselect\b"),
        re.compile(r"(?i)\bor\b\s+1\s*=\s*1"),
        re.compile(r"(?i)\band\b\s+\d+\s*=\s*\d+"),
        re.compile(r"(?i)(sleep|benchmark|pg_sleep|waitfor\s+delay)\s*\("),
        re.compile(r"(?i)(information_schema|load_file|into\s+outfile)"),
        re.compile(r"(--|#|;).*(drop|delete|update|insert)\b", re.IGNORECASE),
        re.compile(r"['\"]\s*(or|and)\s*['\"]?\d"),
    ]

    # Cross-Site Scripting : balises et handlers dangereux
    _MOTIFS_XSS = [
        re.compile(r"(?i)<\s*script"),
        re.compile(r"(?i)javascript\s*:"),
        re.compile(r"(?i)on(error|load|click|mouseover|focus)\s*="),
        re.compile(r"(?i)<\s*iframe"),
        re.compile(r"(?i)(document\.cookie|document\.write|eval\s*\()"),
        re.compile(r"(?i)<\s*img[^>]+src\s*=\s*['\"]?\s*x"),
    ]

    # Traversée de chemin / inclusion de fichiers
    _MOTIFS_TRAVERSEE = [
        re.compile(r"\.\./|\.\.\\"),
        re.compile(r"(?i)(etc/passwd|boot\.ini|/proc/self)"),
        re.compile(r"(?i)(php://|file://|data://)"),
    ]

    def __init__(self,
                 limite_par_minute=120,
                 fenetre_ddos_s=10,
                 seuil_ddos=200):
        # ── Rate limiting (token bucket par IP) ──────────────────────────
        self.limite_par_minute = limite_par_minute
        self._compteurs = defaultdict(lambda: deque())  # ip -> timestamps
        self._ip_bloquees = {}                            # ip -> expiration

        # ── Détection DDoS / Megalodon (volume global glissant) ──────────
        self.fenetre_ddos_s = fenetre_ddos_s
        self.seuil_ddos = seuil_ddos
        self._horodatages_globaux = deque()

        # ── État de menace par couche ────────────────────────────────────
        self.menace_par_couche = {c: NiveauMenace.NOMINAL for c in NOMS_COUCHES}
        self.incidents = deque(maxlen=500)  # journal immuable en mémoire

        # ── CSRF / signatures : secret de session ────────────────────────
        self._secret_csrf = secrets.token_bytes(32)

        # ── Statistiques cumulées ────────────────────────────────────────
        self.stats = defaultdict(int)

    # ═══════════════════════════════════════════════════════════════════
    #  COUCHE 1 — Protection réseau : rate limiting + détection DDoS
    # ═══════════════════════════════════════════════════════════════════
    def autoriser_requete(self, ip, maintenant=None):
        """
        Token bucket par IP. Retourne (autorisee: bool, raison: str).
        Bloque temporairement les IP abusives (réponse anti-DDoS).
        """
        maintenant = maintenant or time.time()

        # IP déjà bloquée ?
        expiration = self._ip_bloquees.get(ip)
        if expiration and maintenant < expiration:
            return False, "ip_bloquee"
        if expiration and maintenant >= expiration:
            del self._ip_bloquees[ip]

        # Nettoyage de la fenêtre glissante (60 s)
        seau = self._compteurs[ip]
        while seau and maintenant - seau[0] > 60:
            seau.popleft()

        if len(seau) >= self.limite_par_minute:
            # Blocage 5 minutes + escalade de menace
            self._ip_bloquees[ip] = maintenant + 300
            self._journaliser("rate_limit_depasse", COUCHE_SURFACE, ip=ip)
            return False, "rate_limit"

        seau.append(maintenant)

        # Volume global → détection DDoS distribué (Megalodon-like)
        self._horodatages_globaux.append(maintenant)
        while (self._horodatages_globaux and
               maintenant - self._horodatages_globaux[0] > self.fenetre_ddos_s):
            self._horodatages_globaux.popleft()

        if len(self._horodatages_globaux) >= self.seuil_ddos:
            self.menace_par_couche[COUCHE_SURFACE] = NiveauMenace.CRITIQUE
            self._journaliser("ddos_detecte", COUCHE_SURFACE,
                              volume=len(self._horodatages_globaux))

        return True, "ok"

    # ═══════════════════════════════════════════════════════════════════
    #  COUCHE 2 — Sécurité applicative : SQLi / XSS / traversée
    # ═══════════════════════════════════════════════════════════════════
    def analyser_charge_utile(self, donnees, couche=COUCHE_SURFACE):
        """
        Inspecte une charge utile (URL, body, header) à la recherche
        d'injections. Retourne un dict de verdict.
        """
        if donnees is None:
            return {"sure": True, "menaces": []}

        texte = donnees if isinstance(donnees, str) else str(donnees)
        menaces = []

        if any(m.search(texte) for m in self._MOTIFS_SQLI):
            menaces.append("sqli")
        if any(m.search(texte) for m in self._MOTIFS_XSS):
            menaces.append("xss")
        if any(m.search(texte) for m in self._MOTIFS_TRAVERSEE):
            menaces.append("traversee_chemin")

        if menaces:
            self.menace_par_couche[couche] = max(
                self.menace_par_couche[couche], NiveauMenace.ELEVE
            )
            for t in menaces:
                self._journaliser(f"injection_{t}", couche,
                                  extrait=texte[:80])

        return {"sure": not menaces, "menaces": menaces}

    def assainir_sortie(self, texte):
        """Échappement HTML (anti-XSS stocké) pour tout contenu utilisateur."""
        if not isinstance(texte, str):
            texte = str(texte)
        return (texte.replace("&", "&amp;")
                     .replace("<", "&lt;")
                     .replace(">", "&gt;")
                     .replace('"', "&quot;")
                     .replace("'", "&#x27;"))

    # ═══════════════════════════════════════════════════════════════════
    #  COUCHE 3 — En-têtes de sécurité + CSRF
    # ═══════════════════════════════════════════════════════════════════
    def entetes_securite(self):
        """En-têtes HTTP durcis (OWANP recommandés) à injecter dans chaque réponse."""
        return {
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
            "Content-Security-Policy": (
                "default-src 'self'; "
                "script-src 'self'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "frame-ancestors 'none'; "
                "base-uri 'self'; form-action 'self'"
            ),
            "X-Frame-Options": "DENY",
            "X-Content-Type-Options": "nosniff",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
        }

    def generer_jeton_csrf(self, session_id):
        """Jeton CSRF lié à la session (double-submit, signé HMAC)."""
        message = f"{session_id}:{int(time.time())}".encode()
        signature = hmac.new(self._secret_csrf, message, hashlib.sha256).hexdigest()
        return f"{message.decode()}:{signature}"

    def valider_jeton_csrf(self, jeton, session_id, age_max_s=3600):
        """Vérifie un jeton CSRF (intégrité + fraîcheur)."""
        try:
            sid, horodatage, signature = jeton.rsplit(":", 2)
        except ValueError:
            return False
        if sid != session_id:
            return False
        if time.time() - int(horodatage) > age_max_s:
            return False
        message = f"{sid}:{horodatage}".encode()
        attendu = hmac.new(self._secret_csrf, message, hashlib.sha256).hexdigest()
        return hmac.compare_digest(attendu, signature)

    # ═══════════════════════════════════════════════════════════════════
    #  PONT AVEC LA FORMULE COGNITIVE  P(t) = Σ αᵢ·Sᵢ(t)·Fᵢ(t)·C_t
    # ═══════════════════════════════════════════════════════════════════
    def facteur_securite_couche(self, couche):
        """
        Traduit le niveau de menace d'une couche en MULTIPLICATEUR de
        sécurité Sᵢ(t) ∈ ]0,1]. Plus la menace est forte, plus Sᵢ chute :
        l'orchestrateur reportera alors le poids vers les couches saines.
        """
        return {
            NiveauMenace.NOMINAL: 1.00,
            NiveauMenace.SURVEILLANCE: 0.92,
            NiveauMenace.ELEVE: 0.75,
            NiveauMenace.CRITIQUE: 0.50,
        }[self.menace_par_couche[couche]]

    def niveau_menace_global(self):
        """Menace maximale toutes couches confondues."""
        return max(self.menace_par_couche.values())

    def facteur_cognitif_recommande(self):
        """
        C_t recommandé : l'IA accélère son adaptation quand la menace monte.
        Nominal → 1.0 ; Critique → 1.45 (réflexe défensif maximal).
        """
        return {
            NiveauMenace.NOMINAL: 1.00,
            NiveauMenace.SURVEILLANCE: 1.10,
            NiveauMenace.ELEVE: 1.25,
            NiveauMenace.CRITIQUE: 1.45,
        }[self.niveau_menace_global()]

    def ponderation_adaptative(self, alpha_nominal):
        """
        Réajuste les coefficients αᵢ : on retire du poids aux couches
        attaquées pour le redistribuer aux couches saines (résilience).
        Renvoie une nouvelle liste α normalisée (Σα = 1).
        """
        poids = list(alpha_nominal)
        for couche in range(len(poids)):
            menace = self.menace_par_couche.get(couche, NiveauMenace.NOMINAL)
            if menace >= NiveauMenace.ELEVE:
                poids[couche] *= 0.4  # forte décote de la couche compromise
            elif menace == NiveauMenace.SURVEILLANCE:
                poids[couche] *= 0.8
        total = sum(poids) or 1.0
        return [p / total for p in poids]

    # ═══════════════════════════════════════════════════════════════════
    #  Cicatrisation : la menace retombe naturellement avec le temps
    # ═══════════════════════════════════════════════════════════════════
    def decroissance_menace(self):
        """
        Fait redescendre d'un cran chaque couche (auto-cicatrisation).
        À appeler périodiquement par l'orchestrateur.
        """
        for couche, niveau in self.menace_par_couche.items():
            if niveau > NiveauMenace.NOMINAL:
                self.menace_par_couche[couche] = NiveauMenace(niveau - 1)

    # ═══════════════════════════════════════════════════════════════════
    #  Journalisation + rapport
    # ═══════════════════════════════════════════════════════════════════
    def _journaliser(self, type_evenement, couche, **details):
        self.stats[type_evenement] += 1
        self.incidents.append({
            "timestamp": datetime.now().isoformat(),
            "evenement": type_evenement,
            "couche": NOMS_COUCHES.get(couche, str(couche)),
            "niveau_menace": int(self.menace_par_couche[couche]),
            **details,
        })

    def rapport(self):
        """Rapport synthétique pour supervision / dashboard."""
        return {
            "timestamp": datetime.now().isoformat(),
            "menace_globale": self.niveau_menace_global().name,
            "menace_par_couche": {
                NOMS_COUCHES[c]: n.name for c, n in self.menace_par_couche.items()
            },
            "facteur_cognitif_recommande": self.facteur_cognitif_recommande(),
            "ip_actuellement_bloquees": len(self._ip_bloquees),
            "incidents_recents": list(self.incidents)[-10:],
            "statistiques": dict(self.stats),
        }
