# Guide de Déploiement Décentralisé de PevO

## Table des Matières
1. [Sécurité Évolutive en Ligne](#1-sécurité-évolutive-en-ligne)
2. [Autonomie Complète sur 3 Couches](#2-autonomie-complète-sur-3-couches)
3. [CLI pour Sites Autonomes](#3-cli-pour-sites-autonomes)

---

## 1. Sécurité Évolutive en Ligne

### Architecture de Sécurité Multicouche

```
╔════════════════════════════════════════════════╗
║  IPFS Gateway (Public)                         ║
║  • Stockage décentralisé                       ║
║  • Immuable et censuré-résistant              ║
║  • Multi-réplication P2P                       ║
╚════════════════════════════════════════════════╝
           ↓ (Chiffrement E2E)
╔════════════════════════════════════════════════╗
║  PevO Orchestrateur (Python)                   ║
║  • Gestion des clés de chiffrement             ║
║  • Validation des certificats TLS              ║
║  • Coordination des 3 couches                  ║
╚════════════════════════════════════════════════╝
           ↓ (Blockchain Trust)
╔════════════════════════════════════════════════╗
║  Nœuds Sécurité (Rust + Go)                    ║
║  • Proof of Work (PoW)                         ║
║  • Consensus distribué                         ║
║  • Audit trail immuable                        ║
╚════════════════════════════════════════════════╝
```

### Composants de Sécurité

#### A. Chiffrement E2E (End-to-End)
```bash
# Générer une clé de chiffrement AES-128 (Fernet)
pevo-cli security-gen-cle

# Résultat: Une clé unique pour chiffrer les sites
# Sortie: gAAAAABl...base64...key
```

#### B. Certificats TLS Autosignés
```bash
# Générer un certificat TLS pour un domaine
pevo-cli security-cert monsite.fr

# Résultat:
# - Certificat PEM (valide 365 jours)
# - Clé privée RSA 2048 bits
# - Empreinte SHA256 unique
```

#### C. Blockchain de Confiance Locale
```bash
# Afficher la blockchain de confiance
pevo-cli security-blockchain

# Mécanisme:
# - Chaque déploiement IPFS = 1 bloc
# - Preuve de travail (PoW) avec difficulté 2
# - Hash SHA256 lié au bloc précédent
# - Immuabilité garantie localement
```

### Avantages de la Sécurité Évolutive

| Couche | Technologie | Bénéfices |
|--------|-------------|----------|
| **Stockage** | IPFS | Pas de serveur centralisé, contenu adressé par hash |
| **Transport** | TLS 1.3 | Chiffrement en transit, authentification domaine |
| **Données** | AES-256 | Chiffrement au repos, même si IPFS compromis |
| **Intégrité** | Blockchain | Historique immuable, auditabilité complète |

---

## 2. Autonomie Complète sur 3 Couches

### Architecture des 3 Couches Web

```
┌─────────────────────────────────────────────────────┐
│ COUCHE 1: SURFACE (Frontend Public)                 │
│ ✓ IPFS Gateway (décentralisé)                       │
│ ✓ Accessible via https://ipfs.io/ipfs/{hash}       │
│ ✓ Consulté worldwide sans limitation               │
│ ✓ 0€ de coût d'hébergement                          │
└─────────────────────────────────────────────────────┘
         ↓ Synchronisation P2P
┌─────────────────────────────────────────────────────┐
│ COUCHE 2: DEEP (Réseau Distribué)                   │
│ ✓ Nœud Go sur port 8082                             │
│ ✓ Consensus blockchain distribuée                   │
│ ✓ Découverte de nœuds automatique                   │
│ ✓ Résilience en cas de coupure                      │
└─────────────────────────────────────────────────────┘
         ↓ Orchestration sécurisée
┌─────────────────────────────────────────────────────┐
│ COUCHE 3: DARKNET (Sécurité Bas Niveau)             │
│ ✓ Nœud Rust sur port 8081                           │
│ ✓ Chiffrement XOR base + AES optionnel              │
│ ✓ Validation des certificats                        │
│ ✓ Audit trail immuable                              │
└─────────────────────────────────────────────────────┘
```

### Sans Aucun Serveur Physique

#### Option A: Configuration IPFS Pure (Recommandée)

```bash
# 1. Installer IPFS
curl https://dist.ipfs.io/go-ipfs/v0.26.0/go-ipfs_v0.26.0_linux-amd64.tar.gz | tar xz
sudo mv go-ipfs/ipfs /usr/local/bin/

# 2. Initialiser IPFS
ipfs init

# 3. Démarrer le nœud IPFS local
ipfs daemon &

# 4. Ajouter votre site
pevo-cli add "mon-blog" ~/sites/mon-blog

# 5. Déployer sur IPFS
pevo-cli deploy-ipfs "mon-blog"

# 6. Site accessible immédiatement via:
# https://ipfs.io/ipfs/{hash}
# https://gateway.ipfs.io/ipfs/{hash}
```

**Avantages:**
- ✅ Zéro serveur physique
- ✅ Coût: 0€ (bande passante IPFS partagée)
- ✅ Données non contrôlées par un tiers
- ✅ Persiste tant que 1 nœud héberge le contenu

#### Option B: IPFS + Nœud Personnel (Plus Résilient)

```bash
# 1. Déployer l'orchestrateur PevO
python3 pevo.py &

# 2. Démarrer les nœuds spécialisés
cd nodes/darknet_node && cargo build --release && ./target/release/darknet_node &
cd nodes/deep_node && go build -o deep_node && ./deep_node &

# 3. Ajouter site + déployer
pevo-cli add "mon-site" ~/sites/mon-site
pevo-cli deploy-ipfs "mon-site"

# 4. Votre nœud IPFS local héberge le contenu
# → Contributions au réseau IPFS
# → Réplication P2P garantie
```

**Avantages:**
- ✅ Contrôle total de l'infrastructure
- ✅ Réplication P2P vers d'autres nœuds
- ✅ Pas d'intermédiaire (gateway.ipfs.io)
- ✅ Bande passante distribuée

### Avec Domaine & IP Dynamique (DuckDNS)

#### Configuration DuckDNS

```bash
# 1. S'inscrire sur DuckDNS
# Aller à: https://www.duckdns.org
# Créer compte → Générer TOKEN

# 2. Configurer avec PevO
pevo-cli dyndns-duckdns "monsite" "TOKEN_DUCKDNS"

# 3. Résultat: domaine stable
# monsite.duckdns.org → IP dynamique mise à jour auto

# 4. Accès au site via le domaine
# https://monsite.duckdns.org
```

#### Mise à Jour Automatique (Cron)

```bash
# Générer commande cron
pevo-cli dyndns-duckdns "monsite" "TOKEN" > /tmp/dyndns.cron

# Ajouter au crontab (mise à jour toutes les 30 min)
(crontab -l 2>/dev/null; echo "*/30 * * * * python3 /chemin/pevo-cli.py dyndns-duckdns monsite TOKEN") | crontab -

# Vérifier le statut
pevo-cli dyndns-status
```

#### Architecture Finale

```
Internet (N'importe où) 
         ↓ HTTPS
    monsite.duckdns.org
         ↓ Redirection DNS dynamique
    Votre IP locale (192.168.1.x:8080)
         ↓
    IPFS Gateway Local
         ↓
    Contenu du site (immuable)
```

---

## 3. CLI pour Sites Autonomes

### Installation

```bash
# 1. Cloner le repo PevO
git clone https://github.com/yourusername/pevo.git
cd pevo

# 2. Installer dépendances Python
pip install cryptography requests

# 3. Rendre la CLI exécutable
chmod +x pevo-cli.py
sudo ln -s $(pwd)/pevo-cli.py /usr/local/bin/pevo-cli
```

### Usage Complet

#### COUCHE 1: Ajouter un Site

```bash
# Format: pevo-cli add <nom> <chemin>
pevo-cli add "mon-portfolio" ~/sites/portfolio

# Résultat:
# ✅ Site 'mon-portfolio' ajouté avec succès
#    Chemin: /home/user/.pevo/sites/mon-portfolio
#    Hash contenu: a3b2c1d4e5f6
```

#### COUCHE 2: Déployer sur IPFS

```bash
# Déployer le site
pevo-cli deploy-ipfs "mon-portfolio"

# Résultat:
# 📤 Déploiement sur IPFS de 'mon-portfolio'...
# ✅ Site déployé sur IPFS!
#    IPFS Hash: QmXxxx...64 caractères...
#    Lien IPFS: https://ipfs.io/ipfs/QmXxxx...
```

#### COUCHE 3: Configurer Domaine & Sécurité

```bash
# Option A: DuckDNS (Automatique)
pevo-cli dyndns-duckdns "monsite" "a1b2c3d4-xxxx-xxxx-xxxx"

# Option B: DynDNS Local
pevo-cli dyndns-config "monsite.local"

# Générer certificat TLS
pevo-cli security-cert "monsite.duckdns.org"

# Résultat:
# 🔒 Certificat TLS généré:
#    Domaine: monsite.duckdns.org
#    Certificat: /home/user/.pevo/security/certs/monsite.duckdns.org.pem
#    Clé: /home/user/.pevo/security/certs/monsite.duckdns.org.key
#    Valide jusqu: 2025-05-26T...
```

### Accès Partout où Internet est Disponible

#### URLs d'Accès

```bash
# Obtenir toutes les URLs d'accès
pevo-cli get-url "mon-portfolio"

# Résultat:
# 🌐 URLs D'ACCÈS - mon-portfolio
#    ipfs: https://ipfs.io/ipfs/QmXxxx...
#    ipfs_gateway: https://gateway.ipfs.io/ipfs/QmXxxx...
#    dyndns: https://monsite.duckdns.org
#    local_gateway: http://localhost:8080/ipfs/QmXxxx...
```

#### Accès Global

| Lieu | Méthode | Lien |
|------|---------|------|
| **N'importe où** | IPFS Public | `https://ipfs.io/ipfs/QmXxxx...` |
| **Réseau mondial** | Gateway IPFS | `https://gateway.ipfs.io/ipfs/QmXxxx...` |
| **Depuis domicile** | DynDNS | `https://monsite.duckdns.org` |
| **Offline** | Cache local | Cache navigateur du hash IPFS |

### Gestion Complète

```bash
# Lister tous les sites enregistrés
pevo-cli list

# Résultat:
# ================================================================================
# 📋 SITES AUTONOMES DÉCENTRALISÉS
# ================================================================================
# 
# 🌐 mon-portfolio
#    Status: ipfs_deployed
#    Hash contenu: a3b2c1d4e5f6
#    IPFS: QmXxxx...
#    Lien: https://ipfs.io/ipfs/QmXxxx...
#    Créé: 2024-05-25T...
#    Sécurité: AES-256
```

```bash
# Voir les statistiques globales
pevo-cli stats

# Résultat:
# 📊 STATISTIQUES PEVO
#    Total sites: 3
#    Déployés IPFS: 2
#    DynDNS configurés: 1
```

```bash
# Vérifier l'intégrité d'un site
pevo-cli verify "mon-portfolio"

# Résultat:
# ✅ Intégrité vérifiée pour 'mon-portfolio'
```

### Exemple Workflow Complet

```bash
# 1. Créer un site simple
mkdir ~/mon-site
cat > ~/mon-site/index.html << 'EOF'
<html>
  <h1>Mon Site Autonome</h1>
  <p>Hébergé sur IPFS, sans serveur physique!</p>
</html>
EOF

# 2. L'ajouter à PevO
pevo-cli add "mon-site" ~/mon-site

# 3. Le déployer sur IPFS
pevo-cli deploy-ipfs "mon-site"

# 4. Configurer un domaine DynDNS
pevo-cli dyndns-duckdns "monsite" "MON_TOKEN_DUCKDNS"

# 5. Générer un certificat TLS
pevo-cli security-cert "monsite.duckdns.org"

# 6. Afficher les URLs d'accès
pevo-cli get-url "mon-site"

# 7. Vérifier l'intégrité
pevo-cli verify "mon-site"

# ✅ Site complètement autonome, accessible partout!
```

---

## Résumé des 3 Réponses

### ❓ Q1: Comment le mettre en ligne en tenant compte de sa sécurité évolutive?

**Réponse:** Architecture multi-couche avec:
- 🔒 **Chiffrement E2E** (AES-128 Fernet)
- 🔐 **Certificats TLS** autosignés/LetsEncrypt
- ⛓️ **Blockchain de confiance** locale (PoW)
- 📊 **Audit trail** immuable de tous les déploiements

### ❓ Q2: Rendre autonome sur 3 couches sans serveur physique?

**Réponse:** Infrastructure décentralisée:
- **Couche 1** (Surface): IPFS Gateway public (0€)
- **Couche 2** (Deep): Nœud Go distribué + consensus
- **Couche 3** (Darknet): Nœud Rust + sécurité bas niveau
- **DNS Dynamique**: DuckDNS pour domaine stable avec IP changeante

### ❓ Q3: CLI pour ajouter sites gratuitement & accessibles partout?

**Réponse:** `pevo-cli` avec 3 commandes simples:
```bash
pevo-cli add "nom" /chemin          # Ajouter site
pevo-cli deploy-ipfs "nom"          # Déployer IPFS
pevo-cli dyndns-duckdns "nom" TOKEN # Domaine stable
```
→ Site accessible via HTTPS partout avec domaine + certificat TLS!

---

## Coûts

| Composant | Coût |
|-----------|------|
| Stockage IPFS | **0€** (P2P distribué) |
| Domaine DuckDNS | **0€** (gratuit) |
| Certificats TLS | **0€** (autosignés) |
| Bande passante | **0€** (P2P) |
| **TOTAL** | **0€** |

**Infrastructure entièrement gratuite & autonome! 🎉**
