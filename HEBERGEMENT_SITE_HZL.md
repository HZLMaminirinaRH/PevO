# 🚀 Hébergement du Site HZLMaminirinaRH sur PevO

## ✅ Étape 1: Site Ajouté à PevO ✓

Ton site a été **enregistré avec succès** dans PevO:

```
Site: hzlmaminirinarh-portfolio
Chemin: /root/.pevo/sites/hzlmaminirinarh-portfolio
Hash contenu: 6da8a159e9c78c3f
Status: local
```

**Fichiers du site:**
- ✅ index.html (page d'accueil)
- ✅ about.html
- ✅ contact.html
- ✅ service.html
- ✅ vision.html
- ✅ politiques.html
- ✅ style.css
- ✅ script.js
- ✅ Fond.jpg (237 KB)
- ✅ F.png (954 KB)

---

## 📡 Étape 2: Déployer sur IPFS (À Faire sur PC Terminal)

### Préalable: Installer IPFS

```bash
# Télécharger et installer IPFS
curl https://dist.ipfs.io/go-ipfs/v0.26.0/go-ipfs_v0.26.0_linux-amd64.tar.gz | tar xz
sudo mv go-ipfs/ipfs /usr/local/bin/

# Initialiser IPFS (première fois uniquement)
ipfs init

# Démarrer le nœud IPFS (laisser tourner en arrière-plan)
ipfs daemon &
```

### Déployer le Site

```bash
# Aller dans le répertoire PevO
cd ~/PevO

# Déployer sur IPFS
python3 pevo-cli.py deploy-ipfs "hzlmaminirinarh-portfolio"

# Résultat attendu:
# ✅ Site déployé sur IPFS!
#    IPFS Hash: QmXxxx...
#    Lien IPFS: https://ipfs.io/ipfs/QmXxxx...
```

---

## 🌐 Étape 3: Accéder au Site Déployé

### URLs d'Accès (Une fois déployé)

```bash
# Obtenir toutes les URLs
python3 pevo-cli.py get-url "hzlmaminirinarh-portfolio"

# Résultat attendu:
# 🌐 URLs D'ACCÈS - hzlmaminirinarh-portfolio
#    ipfs: https://ipfs.io/ipfs/QmXxxx...
#    ipfs_gateway: https://gateway.ipfs.io/ipfs/QmXxxx...
#    dyndns: https://mondomaine.duckdns.org (si configuré)
#    local_gateway: http://localhost:8080/ipfs/QmXxxx...
```

### Solutions Si Lien Bloqué

Si `ipfs.io` ne fonctionne pas:

```bash
# Tester les gateways alternatifs
python3 pevo-cli.py test-gateways "hzlmaminirinarh-portfolio"

# Générer une page HTML avec 10 liens de secours
python3 pevo-cli.py generate-access-page "hzlmaminirinarh-portfolio"

# Épingler sur Web3.storage pour fiabilité 24/7
python3 pevo-cli.py web3-token "YOUR_WEB3STORAGE_TOKEN"
python3 pevo-cli.py web3-pin "hzlmaminirinarh-portfolio"
```

---

## 🔐 Étape 4: Ajouter un Domaine Gratuit (Optionnel)

```bash
# S'inscrire sur DuckDNS: https://www.duckdns.org
# Copier le TOKEN généré

# Configurer le domaine
python3 pevo-cli.py dyndns-duckdns "hzlmaminirinarh" "YOUR_DUCKDNS_TOKEN"

# Résultat:
# ✅ Domaine: hzlmaminirinarh.duckdns.org
#    Accessible: https://hzlmaminirinarh.duckdns.org
```

---

## 📊 Résumé du Déploiement

### Avant (GitHub Pages)
```
URL: https://hzlmaminirinarh.github.io/index.html
Serveur: GitHub (centralisé)
Dépendance: GitHub (peut être supprimé)
Coût: Gratuit mais limité
```

### Après (PevO + IPFS)
```
URL 1: https://ipfs.io/ipfs/QmXxxx...           (IPFS)
URL 2: https://gateway.ipfs.io/ipfs/QmXxxx...  (Gateway alt)
URL 3: https://dweb.link/ipfs/QmXxxx...        (Cloudflare)
URL 4: https://mondomaine.duckdns.org          (Domaine personnel)
URL 5: http://localhost:8080/ipfs/QmXxxx...    (Local)
+ 5 autres URLs alternatives

Serveur: Décentralisé (IPFS P2P)
Dépendance: Aucune (immuable)
Coût: 0€ permanent
Fiabilité: 99.9% (Web3.storage)
```

---

## 🎯 Étapes Rapides (Copy-Paste)

```bash
# 1. Installer IPFS (une seule fois)
curl https://dist.ipfs.io/go-ipfs/v0.26.0/go-ipfs_v0.26.0_linux-amd64.tar.gz | tar xz
sudo mv go-ipfs/ipfs /usr/local/bin/
ipfs init
ipfs daemon &

# 2. Déployer le site
cd ~/PevO
python3 pevo-cli.py deploy-ipfs "hzlmaminirinarh-portfolio"

# 3. Ajouter domaine (optionnel)
python3 pevo-cli.py dyndns-duckdns "hzlmaminirinarh" "TOKEN"

# 4. Obtenir URLs d'accès
python3 pevo-cli.py get-url "hzlmaminirinarh-portfolio"

# ✅ SITE EN LIGNE DÉCENTRALISÉ! 🚀
```

---

## ✨ Avantages

✅ **Gratuit** (0€/an)
✅ **Immuable** (contenu censuré-résistant)
✅ **Décentralisé** (aucun serveur centralisé)
✅ **Résilient** (fonctionne même si ton PC s'éteint avec Web3.storage)
✅ **Rapide** (réseau P2P IPFS)
✅ **Accessible partout** (10+ URLs alternatives)
✅ **Personnalisé** (domaine gratuit DuckDNS)

---

## 🆘 Troubleshooting

### Erreur: "ipfs command not found"
```bash
# Réinstaller IPFS
curl https://dist.ipfs.io/go-ipfs/v0.26.0/go-ipfs_v0.26.0_linux-amd64.tar.gz | tar xz
sudo mv go-ipfs/ipfs /usr/local/bin/ipfs
```

### Erreur: "IPFS daemon not running"
```bash
# Lancer le daemon
ipfs daemon &

# Ou en arrière-plan avec nohup
nohup ipfs daemon > ~/.ipfs/daemon.log 2>&1 &
```

### Lien IPFS ne fonctionne pas
```bash
# Essayer une autre gateway
python3 pevo-cli.py test-gateways "hzlmaminirinarh-portfolio"

# Ou utiliser Web3.storage
python3 pevo-cli.py web3-pin "hzlmaminirinarh-portfolio"
```

---

## 📚 Documentation Connexe

- [LIEN_NON_PRIS_EN_CHARGE.md](./LIEN_NON_PRIS_EN_CHARGE.md) - Si lien bloqué
- [ALTERNATIVES_IPFS.md](./ALTERNATIVES_IPFS.md) - 4 solutions alternatives
- [QUICKSTART.md](./QUICKSTART.md) - Démarrage rapide
- [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) - Guide complet

---

**Ton site GitHub Pages est maintenant prêt à être hébergé sur PevO!** 🎉

Sur PC terminal, exécute les commandes copy-paste ci-dessus et ton site sera décentralisé et en ligne!
