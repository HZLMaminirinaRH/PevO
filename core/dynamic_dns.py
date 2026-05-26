"""
Gestion DNS Dynamique pour IPFS
Maintient à jour le FQDN même avec une IP dynamique
"""

import os
import json
import requests
import subprocess
import socket
from datetime import datetime
from pathlib import Path


class GestionnaireDynDNS:
    """Gère les mises à jour DNS dynamiques pour les sites IPFS"""

    def __init__(self):
        self.config_dir = Path.home() / ".pevo" / "dyndns"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "dyndns_config.json"
        self.ip_history = self.config_dir / "ip_history.json"

        self._charger_config()

    def _charger_config(self):
        """Charge la configuration DynDNS"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                'domaines': [],
                'provider': 'duckdns',
                'derniere_mise_a_jour': None
            }
            self._sauvegarder_config()

    def _sauvegarder_config(self):
        """Sauvegarde la configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

    def _charger_historique_ip(self):
        """Charge l'historique des IP"""
        if self.ip_history.exists():
            with open(self.ip_history, 'r') as f:
                return json.load(f)
        return {'adresses': []}

    def _sauvegarder_historique_ip(self, historique):
        """Sauvegarde l'historique"""
        with open(self.ip_history, 'w') as f:
            json.dump(historique, f, indent=2)

    def obtenir_ip_publique(self):
        """
        Obtient l'adresse IP publique actuelle

        Returns:
            str: Adresse IP publique
        """
        services = [
            'https://api.ipify.org?format=json',
            'https://checkip.amazonaws.com',
            'https://ifconfig.me',
        ]

        for service in services:
            try:
                response = requests.get(service, timeout=5)
                if service == services[0]:  # ipify
                    return response.json()['ip']
                else:
                    return response.text.strip()
            except Exception:
                continue

        # Fallback: obtenir l'IP locale
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return '0.0.0.0'

    def enregistrer_domaine_duckdns(self, domaine, token_duckdns, ipv4=None):
        """
        Enregistre un domaine sur DuckDNS

        Args:
            domaine (str): Nom du domaine (sans .duckdns.org)
            token_duckdns (str): Token d'authentification DuckDNS
            ipv4 (str): Adresse IP (None = IP actuelle)

        Returns:
            dict: Résultat de l'enregistrement
        """
        if not ipv4:
            ipv4 = self.obtenir_ip_publique()

        url = f"https://www.duckdns.org/update"
        params = {
            'domains': domaine,
            'token': token_duckdns,
            'ip': ipv4,
            'verbose': 'true'
        }

        try:
            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200 and 'OK' in response.text:
                # Enregistrer dans la configuration
                entree = {
                    'domaine': f"{domaine}.duckdns.org",
                    'provider': 'duckdns',
                    'ipv4': ipv4,
                    'timestamp': datetime.now().isoformat(),
                    'status': 'actif'
                }

                # Vérifier si le domaine existe déjà
                domaines_existants = [d for d in self.config['domaines'] if d['domaine'] != f"{domaine}.duckdns.org"]
                domaines_existants.append(entree)
                self.config['domaines'] = domaines_existants
                self.config['derniere_mise_a_jour'] = datetime.now().isoformat()
                self._sauvegarder_config()

                # Enregistrer dans l'historique
                historique = self._charger_historique_ip()
                historique['adresses'].append({
                    'domaine': f"{domaine}.duckdns.org",
                    'ipv4': ipv4,
                    'timestamp': datetime.now().isoformat()
                })
                self._sauvegarder_historique_ip(historique)

                return {
                    'success': True,
                    'domaine': f"{domaine}.duckdns.org",
                    'ipv4': ipv4,
                    'message': f"Domaine enregistré avec succès"
                }
            else:
                return {
                    'success': False,
                    'message': f"DuckDNS erreur: {response.text}"
                }

        except Exception as e:
            return {
                'success': False,
                'message': f"Erreur lors de la mise à jour: {e}"
            }

    def configurer_dyndns_local(self, domaine, port_ipfs=8080):
        """
        Configure un serveur DynDNS local (alternative à DuckDNS)

        Args:
            domaine (str): Domaine à utiliser
            port_ipfs (int): Port IPFS local

        Returns:
            dict: Configuration générée
        """
        ip_actuelle = self.obtenir_ip_publique()

        config_dyndns = {
            'domaine': domaine,
            'ip_publique': ip_actuelle,
            'port_ipfs': port_ipfs,
            'url_acces': f"http://{domaine}:{port_ipfs}",
            'timestamp': datetime.now().isoformat(),
            'type': 'dyndns_local'
        }

        entree = {
            'domaine': domaine,
            'provider': 'local',
            'ipv4': ip_actuelle,
            'timestamp': datetime.now().isoformat(),
            'status': 'configure'
        }

        self.config['domaines'].append(entree)
        self._sauvegarder_config()

        return config_dyndns

    def obtenir_url_acces_site(self, nom_site, type_acces='ipfs'):
        """
        Génère l'URL d'accès pour un site

        Args:
            nom_site (str): Nom du site
            type_acces (str): 'ipfs' ou 'dyndns'

        Returns:
            dict: URLs d'accès disponibles
        """
        from pathlib import Path
        registry_file = Path.home() / ".pevo" / "sites_registry.json"

        if not registry_file.exists():
            return {'error': 'Aucun site enregistré'}

        with open(registry_file, 'r') as f:
            registry = json.load(f)

        site = next((s for s in registry['sites'] if s['nom'] == nom_site), None)

        if not site:
            return {'error': f"Site '{nom_site}' introuvable"}

        urls = {}

        if type_acces in ['ipfs', 'tous'] and site.get('ipfs_hash'):
            urls['ipfs'] = f"https://ipfs.io/ipfs/{site['ipfs_hash']}"
            urls['ipfs_gateway'] = f"https://gateway.ipfs.io/ipfs/{site['ipfs_hash']}"

        if type_acces in ['dyndns', 'tous'] and site.get('dyndns_domain'):
            urls['dyndns'] = f"https://{site['dyndns_domain']}"

        urls['local_gateway'] = f"http://localhost:8080/ipfs/{site.get('ipfs_hash', 'non_deployé')}"

        return urls

    def mettre_a_jour_periodique(self, domaine, token_duckdns, intervalle_minutes=30):
        """
        Lance une mise à jour périodique du DNS

        Args:
            domaine (str): Domaine DuckDNS
            token_duckdns (str): Token d'authentification
            intervalle_minutes (int): Intervalle entre les mises à jour

        Returns:
            str: Commande à exécuter en cron
        """
        commande = f"""
#!/bin/bash
# Mise à jour DynDNS toutes les {intervalle_minutes} minutes
*/{ intervalle_minutes} * * * * python3 -c "
from core.dynamic_dns import GestionnaireDynDNS
g = GestionnaireDynDNS()
g.enregistrer_domaine_duckdns('{domaine}', '{token_duckdns}')
" >> ~/.pevo/dyndns.log 2>&1
"""
        return commande

    def afficher_status(self):
        """Affiche le statut DynDNS"""
        print("\n🌐 STATUS DNS DYNAMIQUE")
        print("="*50)

        ip_actuelle = self.obtenir_ip_publique()
        print(f"IP Publique actuelle: {ip_actuelle}")

        if self.config['domaines']:
            print(f"\nDomaines configurés: {len(self.config['domaines'])}")
            for domaine in self.config['domaines']:
                print(f"  • {domaine['domaine']} ({domaine['provider']})")
                print(f"    IP: {domaine['ipv4']}")
                print(f"    Status: {domaine['status']}")
        else:
            print("Aucun domaine configuré")

        print("\n" + "="*50 + "\n")
