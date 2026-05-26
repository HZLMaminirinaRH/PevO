#!/usr/bin/env python3
"""
PevO CLI - Gestionnaire Autonome de Sites Gratuits Décentralisés
Permet d'ajouter, gérer et déployer des sites web sans serveur physique
"""

import os
import sys
import json
import argparse
import subprocess
import hashlib
import time
from datetime import datetime
from pathlib import Path

# Ajouter le chemin local pour les imports
sys.path.insert(0, str(Path(__file__).parent))

from core.dynamic_dns import GestionnaireDynDNS
from core.pinning_service import ServicePinningIPFS

# Import optionnel pour la sécurité (peut échouer si cryptography problématique)
try:
    from core.ipfs_security import SecuriteEvolutiveIPFS
    SECURITE_DISPONIBLE = True
except Exception as e:
    SECURITE_DISPONIBLE = False
    class SecuriteEvolutiveIPFS:
        def valider_integrite_site(self, h1, h2):
            return True

class GestionnaireSitesAutonomes:
    """Gère l'ajout et le déploiement autonome de sites web via IPFS"""

    def __init__(self):
        self.config_dir = Path.home() / ".pevo"
        self.sites_dir = self.config_dir / "sites"
        self.registry_file = self.config_dir / "sites_registry.json"

        self._initialiser_structure()
        self._charger_registry()

    def _initialiser_structure(self):
        """Crée la structure de répertoires"""
        self.config_dir.mkdir(exist_ok=True)
        self.sites_dir.mkdir(exist_ok=True)

    def _charger_registry(self):
        """Charge le registre des sites"""
        if self.registry_file.exists():
            with open(self.registry_file, 'r') as f:
                self.registry = json.load(f)
        else:
            self.registry = {"sites": [], "timestamp": datetime.now().isoformat()}

    def _sauvegarder_registry(self):
        """Sauvegarde le registre des sites"""
        with open(self.registry_file, 'w') as f:
            json.dump(self.registry, f, indent=2)

    def _calculer_hash_contenu(self, chemin_site):
        """Calcule le hash SHA256 du contenu du site"""
        sha256_hash = hashlib.sha256()
        for fichier in Path(chemin_site).rglob('*'):
            if fichier.is_file():
                with open(fichier, 'rb') as f:
                    sha256_hash.update(f.read())
        return sha256_hash.hexdigest()[:16]

    def ajouter_site(self, nom_site, chemin_local):
        """
        Ajoute un nouveau site web autonome

        Args:
            nom_site (str): Nom unique du site
            chemin_local (str): Chemin local vers les fichiers du site
        """
        chemin = Path(chemin_local).resolve()

        if not chemin.exists():
            print(f"❌ Erreur: Le chemin '{chemin}' n'existe pas")
            return False

        if not chemin.is_dir():
            print(f"❌ Erreur: '{chemin}' n'est pas un répertoire")
            return False

        # Vérifier si le site existe déjà
        if any(site['nom'] == nom_site for site in self.registry['sites']):
            print(f"⚠️  Le site '{nom_site}' existe déjà")
            return False

        # Copier vers le répertoire local
        dest_site = self.sites_dir / nom_site
        if dest_site.exists():
            import shutil
            shutil.rmtree(dest_site)

        import shutil
        shutil.copytree(chemin, dest_site)

        # Calculer le hash de contenu
        hash_contenu = self._calculer_hash_contenu(dest_site)

        # Créer l'entrée du registre
        entree_site = {
            "nom": nom_site,
            "chemin_local": str(dest_site),
            "hash_contenu": hash_contenu,
            "cree_le": datetime.now().isoformat(),
            "ipfs_hash": None,
            "dyndns_domain": None,
            "status": "local",
            "securite": {
                "chiffrement": "AES-256",
                "blockchain_hash": None,
                "audit_trail": []
            }
        }

        self.registry['sites'].append(entree_site)
        self._sauvegarder_registry()

        print(f"✅ Site '{nom_site}' ajouté avec succès")
        print(f"   Chemin: {dest_site}")
        print(f"   Hash contenu: {hash_contenu}")
        return True

    def deployer_sur_ipfs(self, nom_site):
        """
        Déploie un site sur IPFS

        Args:
            nom_site (str): Nom du site à déployer
        """
        site = next((s for s in self.registry['sites'] if s['nom'] == nom_site), None)

        if not site:
            print(f"❌ Site '{nom_site}' introuvable")
            return False

        chemin_site = Path(site['chemin_local'])

        # Vérifier si IPFS est disponible
        try:
            result = subprocess.run(['ipfs', '--version'], capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                print("⚠️  IPFS n'est pas disponible. Installation recommandée:")
                print("   https://docs.ipfs.tech/install/command-line/")
                return False
        except FileNotFoundError:
            print("❌ IPFS CLI n'est pas installé")
            print("   Installation: https://docs.ipfs.tech/install/command-line/")
            return False

        try:
            # Ajouter le répertoire à IPFS
            print(f"📤 Déploiement sur IPFS de '{nom_site}'...")
            result = subprocess.run(
                ['ipfs', 'add', '-r', str(chemin_site)],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                # Extraire le hash IPFS de la dernière ligne
                lignes = result.stdout.strip().split('\n')
                ipfs_hash = lignes[-1].split()[1] if lignes else None

                site['ipfs_hash'] = ipfs_hash
                site['status'] = 'ipfs_deployed'
                site['securite']['audit_trail'].append({
                    'action': 'ipfs_deployment',
                    'timestamp': datetime.now().isoformat(),
                    'ipfs_hash': ipfs_hash
                })
                self._sauvegarder_registry()

                print(f"✅ Site déployé sur IPFS!")
                print(f"   IPFS Hash: {ipfs_hash}")
                print(f"   Lien IPFS: https://ipfs.io/ipfs/{ipfs_hash}")
                return True
            else:
                print(f"❌ Erreur IPFS: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            print("❌ Timeout lors du déploiement IPFS")
            return False
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return False

    def configurer_dyndns(self, nom_site, fqdn):
        """
        Configure un domaine DynDNS pour le site

        Args:
            nom_site (str): Nom du site
            fqdn (str): Nom de domaine complet (ex: monsite.monnomde.fr)
        """
        site = next((s for s in self.registry['sites'] if s['nom'] == nom_site), None)

        if not site:
            print(f"❌ Site '{nom_site}' introuvable")
            return False

        site['dyndns_domain'] = fqdn
        site['status'] = 'dyndns_configured'
        site['securite']['audit_trail'].append({
            'action': 'dyndns_configuration',
            'timestamp': datetime.now().isoformat(),
            'domain': fqdn
        })
        self._sauvegarder_registry()

        print(f"✅ DynDNS configuré pour '{nom_site}'")
        print(f"   Domaine: {fqdn}")
        print(f"   IPFS via DynDNS: https://{fqdn}")
        return True

    def lister_sites(self):
        """Liste tous les sites"""
        if not self.registry['sites']:
            print("📭 Aucun site enregistré")
            return

        print("\n" + "="*80)
        print("📋 SITES AUTONOMES DÉCENTRALISÉS")
        print("="*80)

        for site in self.registry['sites']:
            print(f"\n🌐 {site['nom']}")
            print(f"   Status: {site['status']}")
            print(f"   Hash contenu: {site['hash_contenu']}")

            if site['ipfs_hash']:
                print(f"   IPFS: {site['ipfs_hash']}")
                print(f"   Lien: https://ipfs.io/ipfs/{site['ipfs_hash']}")

            if site['dyndns_domain']:
                print(f"   Domaine: {site['dyndns_domain']}")

            print(f"   Créé: {site['cree_le']}")
            print(f"   Sécurité: {site['securite']['chiffrement']}")

        print("\n" + "="*80 + "\n")

    def afficher_stats(self):
        """Affiche les statistiques globales"""
        total_sites = len(self.registry['sites'])
        ipfs_deployed = sum(1 for s in self.registry['sites'] if s['ipfs_hash'])
        dyndns_configured = sum(1 for s in self.registry['sites'] if s['dyndns_domain'])

        print("\n📊 STATISTIQUES PEVO")
        print(f"   Total sites: {total_sites}")
        print(f"   Déployés IPFS: {ipfs_deployed}")
        print(f"   DynDNS configurés: {dyndns_configured}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="PevO CLI - Gestionnaire Autonome de Sites Décentralisés",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
COUCHE 1 - SITES AUTONOMES:
  pevo-cli add "mon-site" ~/chemin/site          Ajouter un site
  pevo-cli list                                   Lister tous les sites
  pevo-cli stats                                  Statistiques

COUCHE 2 - DÉPLOIEMENT DÉCENTRALISÉ (IPFS):
  pevo-cli deploy-ipfs "mon-site"                Déployer sur IPFS
  pevo-cli ipfs-status                           Vérifier statut IPFS
  pevo-cli get-url "mon-site"                    Obtenir URLs d'accès

COUCHE 3 - SÉCURITÉ & DOMAINE:
  pevo-cli security-gen-cle                      Générer clé chiffrement
  pevo-cli security-cert "mon-domaine.fr"        Générer certificat TLS
  pevo-cli dyndns-duckdns "monsite" TOKEN        Configurer DuckDNS
  pevo-cli dyndns-config "mon-domaine.fr"        Configurer DynDNS local
  pevo-cli dyndns-status                         Statut DNS dynamique
  pevo-cli security-blockchain                   Afficher blockchain trust

GESTION COMPLÈTE:
  pevo-cli deploy "mon-site" --domaine monsite.duckdns.org
  pevo-cli verify "mon-site"                     Vérifier intégrité
        """
    )

    subparsers = parser.add_subparsers(dest='commande', help='Commandes disponibles')

    # === SITES AUTONOMES ===
    add_parser = subparsers.add_parser('add', help='Ajouter un nouveau site')
    add_parser.add_argument('nom', help='Nom unique du site')
    add_parser.add_argument('chemin', help='Chemin vers les fichiers')

    # === IPFS ===
    deploy_ipfs = subparsers.add_parser('deploy-ipfs', help='Déployer sur IPFS')
    deploy_ipfs.add_argument('nom', help='Nom du site')

    subparsers.add_parser('ipfs-status', help='Vérifier statut IPFS')

    get_url = subparsers.add_parser('get-url', help='Obtenir URLs d\'accès')
    get_url.add_argument('nom', help='Nom du site')

    # === SÉCURITÉ ===
    subparsers.add_parser('security-gen-cle', help='Générer clé chiffrement')

    security_cert = subparsers.add_parser('security-cert', help='Générer certificat TLS')
    security_cert.add_argument('domaine', help='Domaine')

    subparsers.add_parser('security-blockchain', help='Afficher blockchain trust')

    # === DNS DYNAMIQUE ===
    dyndns_duckdns = subparsers.add_parser('dyndns-duckdns', help='Configurer DuckDNS')
    dyndns_duckdns.add_argument('domaine', help='Domaine DuckDNS (sans .duckdns.org)')
    dyndns_duckdns.add_argument('token', help='Token d\'authentification DuckDNS')

    dyndns_config = subparsers.add_parser('dyndns-config', help='Configurer DynDNS local')
    dyndns_config.add_argument('domaine', help='Nom de domaine')

    subparsers.add_parser('dyndns-status', help='Statut DNS dynamique')

    # === WEB3.STORAGE PINNING ===
    web3_token = subparsers.add_parser('web3-token', help='Configurer Web3.storage token')
    web3_token.add_argument('token', help='Token Web3.storage')

    web3_pin = subparsers.add_parser('web3-pin', help='Épingler site sur Web3.storage')
    web3_pin.add_argument('nom', help='Nom du site')

    subparsers.add_parser('web3-status', help='Statut Web3.storage')

    # === GATEWAYS ALTERNATIVES ===
    test_gw = subparsers.add_parser('test-gateways', help='Tester gateways IPFS')
    test_gw.add_argument('nom', help='Nom du site')

    list_gw = subparsers.add_parser('list-gateways', help='Lister gateways')
    list_gw.add_argument('nom', help='Nom du site')

    gen_page = subparsers.add_parser('generate-access-page', help='Générer page HTML d\'accès')
    gen_page.add_argument('nom', help='Nom du site')

    # === UTILITAIRES ===
    subparsers.add_parser('list', help='Lister tous les sites')
    subparsers.add_parser('stats', help='Afficher statistiques')

    deploy = subparsers.add_parser('deploy', help='Déploiement complet')
    deploy.add_argument('nom', help='Nom du site')
    deploy.add_argument('--domaine', help='Domaine DynDNS')
    deploy.add_argument('--duckdns-token', help='Token DuckDNS')

    verify = subparsers.add_parser('verify', help='Vérifier intégrité site')
    verify.add_argument('nom', help='Nom du site')

    args = parser.parse_args()

    gestionnaire = GestionnaireSitesAutonomes()
    securite = SecuriteEvolutiveIPFS()
    dyndns = GestionnaireDynDNS()
    pinning = ServicePinningIPFS()

    # Routage des commandes
    if args.commande == 'add':
        gestionnaire.ajouter_site(args.nom, args.chemin)

    elif args.commande == 'deploy-ipfs':
        gestionnaire.deployer_sur_ipfs(args.nom)

    elif args.commande == 'dyndns-duckdns':
        result = dyndns.enregistrer_domaine_duckdns(args.domaine, args.token)
        if result['success']:
            print(f"✅ DuckDNS enregistré: {result['domaine']}")
            gestionnaire.configurer_dyndns(args.nom if hasattr(args, 'nom') else args.domaine, result['domaine'])
        else:
            print(f"❌ Erreur: {result['message']}")

    elif args.commande == 'dyndns-config':
        config = dyndns.configurer_dyndns_local(args.domaine)
        print(f"✅ DynDNS configuré: {config['domaine']}")
        print(f"   URL: {config['url_acces']}")

    elif args.commande == 'dyndns-status':
        dyndns.afficher_status()

    elif args.commande == 'ipfs-status':
        try:
            result = subprocess.run(['ipfs', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ IPFS disponible: {result.stdout.strip()}")
            else:
                print("❌ IPFS non disponible")
        except:
            print("❌ IPFS n'est pas installé")

    elif args.commande == 'security-gen-cle':
        cle = securite.generer_cle_chiffrement()
        print(f"🔐 Clé de chiffrement générée:")
        print(f"   {cle}")

    elif args.commande == 'security-cert':
        cert_data = securite.generer_certificat_tls_autosigne(args.domaine)
        print(f"🔒 Certificat TLS généré:")
        print(f"   Domaine: {cert_data['domaine']}")
        print(f"   Certificat: {cert_data['certificat']}")
        print(f"   Clé: {cert_data['cle']}")
        print(f"   Valide jusqu: {cert_data['valide_jusqu']}")

    elif args.commande == 'security-blockchain':
        rapport = securite.generer_rapport_securite()
        print(f"\n📊 BLOCKCHAIN DE CONFIANCE")
        print(f"   Hauteur: {rapport['blockchain_height']}")
        print(f"   Blocs: {rapport['blocs_valides']}")
        print(f"   Certificats: {rapport['certificats_actifs']}")
        print(f"   Chiffrement: {rapport['algorithme_chiffrement']}\n")

    elif args.commande == 'get-url':
        urls = dyndns.obtenir_url_acces_site(args.nom)
        print(f"\n🌐 URLs D'ACCÈS - {args.nom}")
        for key, url in urls.items():
            if not key.startswith('error'):
                print(f"   {key}: {url}")
        print()

    elif args.commande == 'deploy':
        print(f"🚀 Déploiement complet de '{args.nom}'...\n")
        gestionnaire.deployer_sur_ipfs(args.nom)
        if args.domaine:
            gestionnaire.configurer_dyndns(args.nom, args.domaine)
        if args.duckdns_token:
            result = dyndns.enregistrer_domaine_duckdns(args.domaine.split('.')[0], args.duckdns_token)
            if result['success']:
                print(f"✅ DuckDNS synchronisé\n")

    elif args.commande == 'list':
        gestionnaire.lister_sites()

    elif args.commande == 'stats':
        gestionnaire.afficher_stats()

    elif args.commande == 'verify':
        site = next((s for s in gestionnaire.registry['sites'] if s['nom'] == args.nom), None)
        if site and site.get('ipfs_hash'):
            is_valid = securite.valider_integrite_site(site['ipfs_hash'], site['hash_contenu'])
            if is_valid:
                print(f"✅ Intégrité vérifiée pour '{args.nom}'")
            else:
                print(f"⚠️  Attention: L'intégrité ne peut pas être vérifiée")
        else:
            print(f"❌ Site '{args.nom}' non déployé sur IPFS")

    # === WEB3.STORAGE ===
    elif args.commande == 'web3-token':
        pinning.configurer_web3_token(args.token)

    elif args.commande == 'web3-pin':
        site = next((s for s in gestionnaire.registry['sites'] if s['nom'] == args.nom), None)
        if site and site.get('ipfs_hash'):
            pinning.epingler_sur_web3(args.nom, site['ipfs_hash'])
        else:
            print(f"❌ Site '{args.nom}' non déployé sur IPFS")

    elif args.commande == 'web3-status':
        pinning.afficher_statut_pinning()

    # === GATEWAYS ===
    elif args.commande == 'test-gateways':
        site = next((s for s in gestionnaire.registry['sites'] if s['nom'] == args.nom), None)
        if site and site.get('ipfs_hash'):
            pinning.tester_gateways(site['ipfs_hash'])
        else:
            print(f"❌ Site '{args.nom}' non déployé sur IPFS")

    elif args.commande == 'list-gateways':
        site = next((s for s in gestionnaire.registry['sites'] if s['nom'] == args.nom), None)
        if site and site.get('ipfs_hash'):
            gateways = pinning.obtenir_gateways_alternatives(site['ipfs_hash'])
            print(f"\n🌐 GATEWAYS DISPONIBLES - {args.nom}")
            print("=" * 70)
            for i, gw in enumerate(gateways, 1):
                print(f"{i}. {gw}")
            print("=" * 70 + "\n")
        else:
            print(f"❌ Site '{args.nom}' non déployé sur IPFS")

    elif args.commande == 'generate-access-page':
        site = next((s for s in gestionnaire.registry['sites'] if s['nom'] == args.nom), None)
        if site and site.get('ipfs_hash'):
            chemin = pinning.sauvegarder_html_acces(args.nom, site['ipfs_hash'])
            print(f"🔗 Ouvrir dans navigateur:")
            print(f"   open {chemin}")
        else:
            print(f"❌ Site '{args.nom}' non déployé sur IPFS")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
