"""
Sécurité évolutive pour IPFS
Gère le chiffrement E2E, les certificats TLS, et la blockchain de confiance
"""

import os
import json
import hashlib
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


class SecuriteEvolutiveIPFS:
    """Gère la sécurité adaptative pour l'infrastructure IPFS décentralisée"""

    def __init__(self):
        self.config_dir = Path.home() / ".pevo" / "security"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.certs_dir = self.config_dir / "certs"
        self.certs_dir.mkdir(exist_ok=True)
        self.blockchain_file = self.config_dir / "blockchain_trust.json"

        self._initialiser_blockchain()

    def _initialiser_blockchain(self):
        """Initialise la blockchain de confiance locale"""
        if not self.blockchain_file.exists():
            self.blockchain = {
                "chaîne": [],
                "nonce": 0,
                "difficulte": 2
            }
            self._sauvegarder_blockchain()
        else:
            with open(self.blockchain_file, 'r') as f:
                self.blockchain = json.load(f)

    def _sauvegarder_blockchain(self):
        """Sauvegarde la blockchain"""
        with open(self.blockchain_file, 'w') as f:
            json.dump(self.blockchain, f, indent=2)

    def generer_cle_chiffrement(self):
        """Génère une clé Fernet pour le chiffrement E2E"""
        return Fernet.generate_key().decode()

    def chiffrer_contenu_site(self, chemin_site, cle_chiffrement):
        """
        Chiffre le contenu d'un site avec la clé fournie

        Args:
            chemin_site (str): Chemin du site
            cle_chiffrement (str): Clé Fernet encodée

        Returns:
            dict: Métadonnées de chiffrement
        """
        cipher = Fernet(cle_chiffrement.encode())
        fichiers_chiffres = []

        for fichier in Path(chemin_site).rglob('*'):
            if fichier.is_file():
                with open(fichier, 'rb') as f:
                    contenu = f.read()

                contenu_chiffre = cipher.encrypt(contenu)

                # Sauvegarder le fichier chiffré
                fichier_dest = Path(str(fichier) + '.enc')
                with open(fichier_dest, 'wb') as f:
                    f.write(contenu_chiffre)

                fichiers_chiffres.append({
                    'original': str(fichier),
                    'chiffre': str(fichier_dest),
                    'hash': hashlib.sha256(contenu).hexdigest()[:16]
                })

        return {
            'timestamp': datetime.now().isoformat(),
            'fichiers': fichiers_chiffres,
            'algorithme': 'Fernet (AES-128)',
            'nombre_fichiers': len(fichiers_chiffres)
        }

    def generer_certificat_tls_autosigne(self, domaine, jours_validite=365):
        """
        Génère un certificat TLS autosigné pour DynDNS

        Args:
            domaine (str): Nom de domaine
            jours_validite (int): Durée de validité en jours

        Returns:
            dict: Chemin du certificat et de la clé
        """
        # Générer une clé privée RSA
        clé_privée = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        # Créer un certificat autosigné
        sujet = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"FR"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Internet"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"Decentralized"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"PevO"),
            x509.NameAttribute(NameOID.COMMON_NAME, domaine),
        ])

        certificat = x509.CertificateBuilder().subject_name(
            sujet
        ).issuer_name(
            issuer
        ).public_key(
            clé_privée.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=jours_validite)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName(domaine),
                x509.DNSName(f"*.{domaine}"),
            ]),
            critical=False,
        ).sign(clé_privée, hashes.SHA256(), default_backend())

        # Sauvegarder le certificat
        chemin_cert = self.certs_dir / f"{domaine}.pem"
        with open(chemin_cert, "wb") as f:
            f.write(certificat.public_bytes(serialization.Encoding.PEM))

        # Sauvegarder la clé privée
        chemin_clé = self.certs_dir / f"{domaine}.key"
        with open(chemin_clé, "wb") as f:
            f.write(clé_privée.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

        return {
            'domaine': domaine,
            'certificat': str(chemin_cert),
            'cle': str(chemin_clé),
            'valide_jusqu': (datetime.utcnow() + timedelta(days=jours_validite)).isoformat(),
            'type': 'autosigne_pevo'
        }

    def ajouter_bloc_blockchain(self, donnees_site):
        """
        Ajoute un bloc à la blockchain de confiance

        Args:
            donnees_site (dict): Données du site à enregistrer

        Returns:
            dict: Bloc créé
        """
        hash_precedent = self.blockchain['chaîne'][-1]['hash'] if self.blockchain['chaîne'] else '0'

        bloc = {
            'index': len(self.blockchain['chaîne']),
            'timestamp': datetime.now().isoformat(),
            'donnees': donnees_site,
            'hash_precedent': hash_precedent,
            'nonce': 0,
            'hash': ''
        }

        # Preuve de travail (Proof of Work simplifié)
        while True:
            bloc_json = json.dumps({
                'index': bloc['index'],
                'timestamp': bloc['timestamp'],
                'donnees': bloc['donnees'],
                'hash_precedent': bloc['hash_precedent'],
                'nonce': bloc['nonce']
            }, sort_keys=True)

            hash_bloc = hashlib.sha256(bloc_json.encode()).hexdigest()

            if hash_bloc.startswith('0' * self.blockchain['difficulte']):
                bloc['hash'] = hash_bloc
                break

            bloc['nonce'] += 1

        self.blockchain['chaîne'].append(bloc)
        self._sauvegarder_blockchain()

        return bloc

    def valider_integrite_site(self, ipfs_hash, hash_attendu):
        """
        Valide l'intégrité d'un site stocké sur IPFS

        Args:
            ipfs_hash (str): Hash IPFS du site
            hash_attendu (str): Hash attendu du contenu

        Returns:
            bool: True si valide
        """
        # Vérifier si le bloc est dans la blockchain
        for bloc in self.blockchain['chaîne']:
            if bloc['donnees'].get('ipfs_hash') == ipfs_hash:
                if bloc['donnees'].get('hash_contenu') == hash_attendu:
                    return True

        return False

    def generer_rapport_securite(self):
        """Génère un rapport de sécurité"""
        return {
            'timestamp': datetime.now().isoformat(),
            'blockchain_height': len(self.blockchain['chaîne']),
            'blocs_valides': len(self.blockchain['chaîne']),
            'certificats_actifs': len(list(self.certs_dir.glob('*.pem'))),
            'algorithme_chiffrement': 'AES-128 (Fernet)',
            'difficulte_proof_of_work': self.blockchain['difficulte']
        }
