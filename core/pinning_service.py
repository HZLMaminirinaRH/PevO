"""
Service de Pinning IPFS Gratuit
Utilise Web3.storage pour garantir que tes fichiers restent en ligne
"""

import os
import json
import requests
import subprocess
from pathlib import Path
from datetime import datetime


class ServicePinningIPFS:
    """Gère le pinning des sites sur Web3.storage (gratuit & fiable)"""

    def __init__(self):
        self.config_dir = Path.home() / ".pevo" / "pinning"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.pinning_registry = self.config_dir / "pinning_registry.json"
        self.web3_token_file = self.config_dir / ".web3storage_token"

        self._charger_registry()

    def _charger_registry(self):
        """Charge le registre de pinning"""
        if self.pinning_registry.exists():
            with open(self.pinning_registry, 'r') as f:
                self.registry = json.load(f)
        else:
            self.registry = {"pinned_sites": []}
            self._sauvegarder_registry()

    def _sauvegarder_registry(self):
        """Sauvegarde le registre"""
        with open(self.pinning_registry, 'w') as f:
            json.dump(self.registry, f, indent=2)

    def configurer_web3_token(self, token):
        """
        Configure le token Web3.storage

        Args:
            token (str): Token d'authentification Web3.storage
        """
        with open(self.web3_token_file, 'w') as f:
            f.write(token)

        print("✅ Token Web3.storage configuré")
        print("   Dossier: " + str(self.config_dir))
        return True

    def obtenir_token(self):
        """Récupère le token Web3.storage"""
        if self.web3_token_file.exists():
            with open(self.web3_token_file, 'r') as f:
                return f.read().strip()
        return None

    def epingler_sur_web3(self, nom_site, ipfs_hash):
        """
        Épingle un site sur Web3.storage pour le garder en ligne

        Args:
            nom_site (str): Nom du site
            ipfs_hash (str): Hash IPFS du site
        """
        token = self.obtenir_token()

        if not token:
            print("❌ Token Web3.storage non configuré")
            print("   Configurer: pevo-cli web3-token <TOKEN>")
            return False

        try:
            # Appeler l'API Web3.storage
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }

            data = {
                "cid": ipfs_hash,
                "name": nom_site
            }

            response = requests.post(
                "https://api.web3.storage/pins",
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code in [200, 201]:
                entree = {
                    "site": nom_site,
                    "ipfs_hash": ipfs_hash,
                    "pinned_on": "web3.storage",
                    "timestamp": datetime.now().isoformat(),
                    "status": "pinned"
                }

                # Ajouter au registre
                if not any(p['site'] == nom_site for p in self.registry['pinned_sites']):
                    self.registry['pinned_sites'].append(entree)
                    self._sauvegarder_registry()

                print(f"✅ Site '{nom_site}' épinglé sur Web3.storage")
                print(f"   IPFS Hash: {ipfs_hash}")
                print(f"   Statut: En ligne 24/7 (même machine éteinte)")
                return True
            else:
                print(f"❌ Erreur Web3.storage: {response.status_code}")
                print(f"   Message: {response.text}")
                return False

        except Exception as e:
            print(f"❌ Erreur lors du pinning: {e}")
            return False

    def obtenir_gateways_alternatives(self, ipfs_hash):
        """
        Génère une liste de gateways IPFS alternatifs

        Args:
            ipfs_hash (str): Hash IPFS

        Returns:
            list: Liste d'URLs alternatives
        """
        gateways = [
            f"https://ipfs.io/ipfs/{ipfs_hash}",
            f"https://gateway.ipfs.io/ipfs/{ipfs_hash}",
            f"https://dweb.link/ipfs/{ipfs_hash}",
            f"https://4everland.io/ipfs/{ipfs_hash}",
            f"https://cloudflare-ipfs.com/ipfs/{ipfs_hash}",
            f"https://cf-ipfs.com/ipfs/{ipfs_hash}",
            f"https://ipfs.infura.io/ipfs/{ipfs_hash}",
            f"https://libp2p.io/ipfs/{ipfs_hash}",
            f"https://nft.storage/ipfs/{ipfs_hash}",
            f"https://w3s.link/ipfs/{ipfs_hash}",  # Web3.storage
        ]
        return gateways

    def tester_gateways(self, ipfs_hash, timeout=5):
        """
        Teste les gateways et retourne les fonctionnels

        Args:
            ipfs_hash (str): Hash IPFS à tester
            timeout (int): Timeout en secondes

        Returns:
            dict: Gateways fonctionnels et non-fonctionnels
        """
        gateways = self.obtenir_gateways_alternatives(ipfs_hash)
        fonctionnels = []
        non_fonctionnels = []

        print(f"\n🔍 Test des gateways IPFS pour {ipfs_hash[:16]}...")
        print("=" * 60)

        for gateway in gateways:
            try:
                response = requests.head(gateway, timeout=timeout)
                if response.status_code == 200:
                    fonctionnels.append(gateway)
                    print(f"✅ {gateway}")
                else:
                    non_fonctionnels.append(gateway)
                    print(f"⚠️  {gateway} ({response.status_code})")
            except Exception as e:
                non_fonctionnels.append(gateway)
                print(f"❌ {gateway} (timeout)")

        print("=" * 60)
        print(f"\n✅ Gateways fonctionnels: {len(fonctionnels)}")
        print(f"❌ Gateways non-fonctionnels: {len(non_fonctionnels)}\n")

        return {
            "fonctionnels": fonctionnels,
            "non_fonctionnels": non_fonctionnels
        }

    def generer_html_acces_multiples(self, nom_site, ipfs_hash):
        """
        Génère une page HTML avec liens vers plusieurs gateways

        Args:
            nom_site (str): Nom du site
            ipfs_hash (str): Hash IPFS

        Returns:
            str: HTML généré
        """
        gateways = self.obtenir_gateways_alternatives(ipfs_hash)

        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Accès Multiplié - {nom_site}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        .container {{
            background: rgba(0,0,0,0.3);
            padding: 30px;
            border-radius: 10px;
        }}
        h1 {{ color: #4fc3f7; }}
        .gateway {{
            margin: 15px 0;
            padding: 15px;
            background: rgba(0,0,0,0.5);
            border-left: 4px solid #4fc3f7;
            border-radius: 5px;
        }}
        .gateway a {{
            color: #81d4fa;
            text-decoration: none;
            word-break: break-all;
        }}
        .gateway a:hover {{
            color: #b3e5fc;
        }}
        .info {{
            margin-top: 30px;
            font-size: 0.9em;
            opacity: 0.8;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 Accès à "{nom_site}"</h1>
        <p>Si l'un des liens ne fonctionne pas, essayez un autre.</p>

        <h2>Gateways IPFS:</h2>
"""

        for i, gateway in enumerate(gateways, 1):
            html += f"""        <div class="gateway">
            <strong>Option {i}:</strong><br>
            <a href="{gateway}" target="_blank">{gateway}</a>
        </div>
"""

        html += """
        <div class="info">
            <p><strong>Hash IPFS:</strong> """ + ipfs_hash + """</p>
            <p>Tous les liens pointent vers le même contenu.
            Si un gateway est lent ou indisponible, essayez un autre.</p>
        </div>
    </div>
</body>
</html>"""

        return html

    def sauvegarder_html_acces(self, nom_site, ipfs_hash, chemin_sortie=None):
        """
        Sauvegarde une page HTML avec accès via plusieurs gateways

        Args:
            nom_site (str): Nom du site
            ipfs_hash (str): Hash IPFS
            chemin_sortie (str): Chemin de sortie (optionnel)
        """
        if not chemin_sortie:
            chemin_sortie = Path.home() / "Bureau" / f"{nom_site}_acces.html"

        html = self.generer_html_acces_multiples(nom_site, ipfs_hash)

        Path(chemin_sortie).parent.mkdir(parents=True, exist_ok=True)
        with open(chemin_sortie, 'w') as f:
            f.write(html)

        print(f"✅ Page d'accès créée: {chemin_sortie}")
        return str(chemin_sortie)

    def afficher_statut_pinning(self):
        """Affiche le statut du pinning"""
        print("\n📌 STATUT PINNING IPFS")
        print("=" * 60)

        if not self.registry['pinned_sites']:
            print("Aucun site épinglé actuellement")
            return

        print(f"Sites épinglés: {len(self.registry['pinned_sites'])}\n")

        for site in self.registry['pinned_sites']:
            print(f"🌐 {site['site']}")
            print(f"   Service: {site['pinned_on']}")
            print(f"   IPFS: {site['ipfs_hash'][:16]}...")
            print(f"   Status: {site['status']}")
            print(f"   Pinné le: {site['timestamp']}\n")

        print("=" * 60)
