# 🚀 PevO Quickstart - Démarrer en 5 Minutes

## ✅ Checklist: Ce que vous avez besoin

- [ ] Une machine (PC, Mac, Raspberry Pi, etc.)
- [ ] Python 3.8+
- [ ] Connexion Internet
- [ ] 10 minutes de temps libre
- [ ] Un token DuckDNS (optionnel pour domaine gratuit)

## 🔧 Étape 1: Installation (2 minutes)

```bash
# Cloner le repo
git clone https://github.com/yourusername/pevo.git
cd pevo

# Installer les dépendances Python
pip install -r requirements.txt

# Rendre pevo-cli exécutable
chmod +x pevo-cli.py

# Créer un lien symbolique (optionnel mais utile)
sudo ln -s $(pwd)/pevo-cli.py /usr/local/bin/pevo-cli
```

✅ **Installation complète!**

## 📝 Étape 2: Créer votre premier site (1 minute)

```bash
# Créer un dossier pour votre site
mkdir ~/mon-premier-site

# Ajouter une page HTML simple
cat > ~/mon-premier-site/index.html << 'HTML'
<!DOCTYPE html>
<html>
  <head>
    <title>Mon Premier Site Autonome</title>
  </head>
  <body>
    <h1>🎉 Mon site est en ligne!</h1>
    <p>Hébergé sur IPFS, gratuit, sans serveur physique.</p>
  </body>
</html>
HTML

# Enregistrer le site dans PevO
pevo-cli add "mon-premier-site" ~/mon-premier-site

# Résultat:
# ✅ Site 'mon-premier-site' ajouté avec succès
```

✅ **Site créé!**

## 🚀 Étape 3: Déployer sur IPFS (2 minutes)

```bash
# D'abord, installer IPFS (une fois)
curl https://dist.ipfs.io/go-ipfs/v0.26.0/go-ipfs_v0.26.0_linux-amd64.tar.gz | tar xz
sudo mv go-ipfs/ipfs /usr/local/bin/

# Démarrer le nœud IPFS (première fois seulement)
ipfs init
ipfs daemon &  # Laisser tourner en arrière-plan

# Déployer le site
pevo-cli deploy-ipfs "mon-premier-site"

# Résultat:
# ✅ Site déployé sur IPFS!
#    IPFS Hash: QmXxxx...64_caractères...
#    Lien IPFS: https://ipfs.io/ipfs/QmXxxx...
```

✅ **SITE EN LIGNE GRATUITEMENT!**

### 🌍 Votre site est maintenant accessible:

```
🔗 https://ipfs.io/ipfs/QmXxxx...
   (Accessible worldwide, gratuit, décentralisé)
```

**Ouvrez ce lien dans votre navigateur → Voilà! 🎉**

---

## 🎁 Bonus: Ajouter un Domaine Gratuit (Optionnel)

### Étape 1: Créer un compte DuckDNS (2 minutes)

1. Aller sur https://www.duckdns.org
2. Cliquer sur **"Sign Up"** (avec GitHub ou autre)
3. Créer un domaine (ex: `monsite`)
4. Copier le **TOKEN** généré

### Étape 2: Configurer avec PevO (30 secondes)

```bash
# Remplacer TOKEN par votre vrai token
pevo-cli dyndns-duckdns "mon-premier-site" "VOTRE_TOKEN_DUCKDNS"

# Résultat:
# ✅ DuckDNS configuré!
#    Domaine: monsite.duckdns.org
#    Accessible: https://monsite.duckdns.org
```

### 🌍 Votre site a maintenant 2 URLs:

```
1. 🔗 https://ipfs.io/ipfs/QmXxxx...
   (IPFS public, très rapide)

2. 🌐 https://monsite.duckdns.org
   (Domaine personnel gratuit)
```

---

## 📊 Vérifier votre Installation

```bash
# Lister tous vos sites
pevo-cli list

# Voir statistiques
pevo-cli stats

# Obtenir URLs d'accès
pevo-cli get-url "mon-premier-site"

# Vérifier intégrité
pevo-cli verify "mon-premier-site"
```

---

## 🎓 Prochaines Étapes

### Approfondir

- Lire **[REPONSES_3_QUESTIONS.md](./REPONSES_3_QUESTIONS.md)** pour comprendre l'architecture
- Lire **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** pour configuration avancée
- Explorer **[ARCHITECTURE.md](./ARCHITECTURE.md)** pour détails techniques

### Ajouter plus de Sites

```bash
# Créer un nouveau site
mkdir ~/mon-blog
echo '<h1>Mon Blog</h1>' > ~/mon-blog/index.html

# L'ajouter et déployer
pevo-cli add "mon-blog" ~/mon-blog
pevo-cli deploy-ipfs "mon-blog"

# Résultat: Deuxième site en ligne!
```

### Sécuriser votre Site

```bash
# Générer une clé de chiffrement
pevo-cli security-gen-cle

# Générer un certificat TLS
pevo-cli security-cert "monsite.duckdns.org"

# Afficher la blockchain de confiance
pevo-cli security-blockchain
```

---

## ❓ FAQ Rapide

### Q: Combien ça coûte?
**A:** 0€ complètement gratuit! (IPFS + DuckDNS gratuits)

### Q: Mon site sera toujours accessible?
**A:** Oui, tant que votre machine est connectée. IPFS garde une copie en cache sur le réseau.

### Q: Je peux modifier mon site après?
**A:** Oui! Modifiez les fichiers, puis redéployez avec `pevo-cli deploy-ipfs`.

### Q: Et si mon IP change?
**A:** DuckDNS met à jour automatiquement. Votre domaine reste stable.

### Q: C'est vraiment décentralisé?
**A:** Oui! IPFS = réseau P2P. Pas de serveur centralisé.

### Q: Puis-je utiliser un vrai domaine (.fr, .com)?
**A:** Oui! Pointez les DNS de votre domaine vers DuckDNS.

---

## 🆘 Troubleshooting

### Erreur: "IPFS non disponible"

```bash
# Vérifier IPFS
ipfs --version

# Si pas trouvé, installer:
curl https://dist.ipfs.io/go-ipfs/v0.26.0/go-ipfs_v0.26.0_linux-amd64.tar.gz | tar xz
sudo mv go-ipfs/ipfs /usr/local/bin/

# Démarrer le daemon
ipfs init
ipfs daemon &
```

### Erreur: "Site introuvable"

```bash
# Vérifier le nom du site
pevo-cli list

# Utiliser le nom exact
pevo-cli deploy-ipfs "nom-exact-du-site"
```

### DuckDNS ne fonctionne pas

```bash
# Vérifier le token
# Assurez-vous que vous avez copié le bon TOKEN

# Tester manuellement
curl "https://www.duckdns.org/update?domains=monsite&token=TOKEN&ip=votre_ip"

# Devrait répondre: OK
```

---

## 📚 Ressources

| Ressource | Lien |
|-----------|------|
| IPFS | https://ipfs.io |
| DuckDNS | https://www.duckdns.org |
| Documentation PevO | Voir README.md |
| Questions? | REPONSES_3_QUESTIONS.md |

---

## ✅ Résumé en 3 Étapes

```bash
# 1. Créer site
mkdir ~/mon-site && echo '<h1>Coucou!</h1>' > ~/mon-site/index.html
pevo-cli add "mon-site" ~/mon-site

# 2. Déployer
pevo-cli deploy-ipfs "mon-site"

# 3. Domaine (optionnel)
pevo-cli dyndns-duckdns "mon-site" "TOKEN"

# ✅ SITE EN LIGNE! 🚀
```

---

**Temps total: ~5 minutes**
**Coût total: 0€**
**Résultat: Site moderne, autonome, décentralisé**

🎉 **Bienvenue dans le futur du web!**
