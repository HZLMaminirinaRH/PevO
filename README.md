# 🚀 PevO - Infrastructure Décentralisée & Autonome

> **L'infrastructure web du futur: gratuite, autonome, sans serveur physique.**

## 🎯 Objectif

PevO résout les **3 défis fondamentaux du web moderne**:

| Défi | Solution |
|------|----------|
| **🔐 Sécurité évolutive en ligne** | Architecture 4 niveaux (chiffrement, TLS, blockchain, audit) |
| **🌍 Autonomie sans serveur physique** | IPFS décentralisé + DynDNS gratuit + 0€ coût |
| **💻 CLI pour sites gratuits partout** | 3 commandes simples, accessible worldwide |

## 📚 Documentation

### 👉 Commencer Ici

- **[REPONSES_3_QUESTIONS.md](./REPONSES_3_QUESTIONS.md)** - Guide complet des 3 réponses (recommandé ⭐)
- **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** - Guide détaillé de déploiement
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - Architecture technique polyglotte

## 🚀 Quickstart (5 minutes)

### Installation

```bash
# 1. Cloner PevO
git clone https://github.com/yourusername/pevo.git && cd pevo

# 2. Installer dépendances
pip install -r requirements.txt

# 3. Rendre CLI exécutable
chmod +x pevo-cli.py && sudo ln -s $(pwd)/pevo-cli.py /usr/local/bin/pevo-cli

# 4. Installer IPFS (optionnel)
curl https://dist.ipfs.io/go-ipfs/v0.26.0/go-ipfs_v0.26.0_linux-amd64.tar.gz | tar xz
sudo mv go-ipfs/ipfs /usr/local/bin/
```

### 3 Commandes pour un Site Gratuit

```bash
# 1. Ajouter un site
mkdir ~/mon-site && echo '<h1>Mon Site!</h1>' > ~/mon-site/index.html
pevo-cli add "mon-site" ~/mon-site

# 2. Déployer sur IPFS (gratuit, décentralisé)
pevo-cli deploy-ipfs "mon-site"

# 3. Domaine gratuit (optionnel)
pevo-cli dyndns-duckdns "monsite" "VOTRE_TOKEN"

# ✅ SITE EN LIGNE GRATUITEMENT!
```

## 💰 Coûts

| Composant | Coût |
|-----------|------|
| Stockage | 0€ (IPFS) |
| Domaine | 0€ (DuckDNS) |
| Certificat TLS | 0€ (autosigné) |
| Bande passante | 0€ (P2P) |
| **TOTAL** | **0€/an** |

## 🏗️ Architecture 3 Couches

```
SURFACE (IPFS)          → Stockage décentralisé gratuit
    ↓
DEEP (Go - 8082)        → Consensus distribué
    ↓
DARKNET (Rust - 8081)   → Sécurité bas niveau
```

## 🔐 Sécurité

✅ Chiffrement E2E (AES-128)
✅ Certificats TLS (RSA-2048)
✅ Blockchain immuable
✅ Audit trail complet
✅ Décentralisé & censuré-résistant

## 📖 Commandes Principales

```bash
# Sites
pevo-cli add "nom" /chemin          # Ajouter
pevo-cli list                        # Lister
pevo-cli deploy-ipfs "nom"          # Déployer IPFS

# Domaine
pevo-cli dyndns-duckdns "nom" TOKEN # Domaine gratuit

# Sécurité
pevo-cli security-cert "domaine"    # Certificat TLS
pevo-cli security-blockchain        # Afficher blockchain
pevo-cli verify "nom"               # Vérifier intégrité
```

## 📝 Documentation Complète

1. **[REPONSES_3_QUESTIONS.md](./REPONSES_3_QUESTIONS.md)** - ⭐ Lire en premier!
   - Q1: Sécurité évolutive en ligne
   - Q2: Autonomie sans serveur physique
   - Q3: CLI pour sites gratuits partout

2. **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** - Guide technique détaillé

3. **[ARCHITECTURE.md](./ARCHITECTURE.md)** - Architecture polyglotte

## 🌍 Accessible Partout

Votre site accessible via:

```
https://ipfs.io/ipfs/QmXxxx...          (IPFS global)
https://gateway.ipfs.io/ipfs/QmXxxx...  (Gateway alternatif)
https://monsite.duckdns.org             (Domaine personnel)
```

## ✨ Résumé

- 🚀 **5 minutes** de configuration
- 💰 **0€** d'investissement
- 🔐 **Grade militaire** de sécurité
- 🌍 **Accessible worldwide**
- 🛡️ **Censuré-résistant** (IPFS)
- 📍 **Autonome** (zéro dépendance)

---

**Le futur du web est décentralisé. PevO le rend possible dès maintenant.**
