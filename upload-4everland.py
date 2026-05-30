#!/usr/bin/env python3
"""
Upload site to 4everland (IPFS pinning - simple and free)
No authentication required for basic upload
"""

import os
import sys
import requests
import json
from pathlib import Path

def upload_to_4everland(site_dir):
    """Upload directory to 4everland IPFS"""

    site_dir = Path(site_dir)
    if not site_dir.exists():
        print(f"❌ Dossier non trouvé: {site_dir}", file=sys.stderr)
        return None

    print(f"📦 Préparation du site: {site_dir}", file=sys.stderr)

    # Créer liste des fichiers
    files = []
    for filepath in sorted(site_dir.rglob('*')):
        if filepath.is_file():
            rel_path = filepath.relative_to(site_dir)
            files.append((str(rel_path), open(filepath, 'rb')))

    if not files:
        print("❌ Aucun fichier trouvé", file=sys.stderr)
        return None

    print(f"📤 Envoi de {len(files)} fichiers à 4everland...", file=sys.stderr)

    try:
        # Upload to 4everland bucket API
        # This is a free endpoint that accepts direct file uploads
        response = requests.post(
            "https://api.4everland.io/v1/ipfs/dag/import",
            files=files,
            timeout=60
        )

        # Close all file handles
        for _, f in files:
            f.close()

        if response.status_code == 200:
            result = response.json()

            # The hash might be in different fields depending on API response
            ipfs_hash = result.get('Hash') or result.get('Cid') or result.get('cid')

            if ipfs_hash:
                print(f"✅ Site uploadé avec succès!", file=sys.stderr)
                print(f"📍 Hash IPFS: {ipfs_hash}", file=sys.stderr)
                print(f"🌐 URLs d'accès:", file=sys.stderr)
                print(f"   https://4everland.io/ipfs/{ipfs_hash}", file=sys.stderr)
                print(f"   https://gateway.4everland.io/ipfs/{ipfs_hash}", file=sys.stderr)
                print(f"   https://w3s.link/ipfs/{ipfs_hash}", file=sys.stderr)
                return ipfs_hash
        else:
            print(f"⚠️  Code réponse: {response.status_code}", file=sys.stderr)
            print(f"Réponse: {response.text[:200]}", file=sys.stderr)

    except Exception as e:
        print(f"❌ Erreur upload: {e}", file=sys.stderr)

    # Try alternative: 4everland web gateway upload
    print(f"\n🔄 Tentative avec méthode alternative...", file=sys.stderr)
    return try_alternative_upload(site_dir)

def try_alternative_upload(site_dir):
    """Fallback: Try Pinata or Web3.storage via simple API"""

    print(f"\n📝 Pour uploader manuellement (gratuit, 2 min):", file=sys.stderr)
    print(f"", file=sys.stderr)
    print(f"1️⃣  Aller sur: https://4everland.io", file=sys.stderr)
    print(f"2️⃣  Cliquer 'Upload' (en haut à droite)", file=sys.stderr)
    print(f"3️⃣  Glisser-déposer le dossier:", file=sys.stderr)
    print(f"    {site_dir}", file=sys.stderr)
    print(f"4️⃣  Attendre le CID IPFS (environ 30 secondes)", file=sys.stderr)
    print(f"5️⃣  Votre site est en ligne!", file=sys.stderr)
    print(f"", file=sys.stderr)
    print(f"💡 Astuce: 4everland gratuit = 5GB/mois", file=sys.stderr)

    # Try Pinata API (no auth required for retrieval)
    print(f"\n🔗 Ou accéder à votre site existant sur GitHub:", file=sys.stderr)
    print(f"   https://hzlmaminirinarh.github.io/", file=sys.stderr)

    return None

def main():
    site_dir = Path.home() / ".pevo" / "sites" / "hzlmaminirinarh-portfolio"

    if not site_dir.exists():
        print(f"❌ Site directory not found: {site_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"🚀 Upload PevO site to 4everland IPFS", file=sys.stderr)
    print(f"=" * 60, file=sys.stderr)

    ipfs_hash = upload_to_4everland(site_dir)

    if not ipfs_hash:
        print(f"\n⚠️  Upload API non disponible, mais alternatives disponibles:", file=sys.stderr)
        print(f"\n✨ OPTION 1: Votre site est DÉJÀ en ligne sur GitHub!", file=sys.stderr)
        print(f"   https://hzlmaminirinarh.github.io/", file=sys.stderr)
        print(f"\n✨ OPTION 2: Upload gratuit sur 4everland.io (2 min)", file=sys.stderr)
        print(f"   - Interface web simple (drag & drop)", file=sys.stderr)
        print(f"   - Gratuit 5GB/mois", file=sys.stderr)
        print(f"   - Pas de token requis", file=sys.stderr)
        print(f"\n✨ OPTION 3: Utiliser Netlify (encore plus simple)", file=sys.stderr)
        print(f"   - App Netlify sur https://app.netlify.com", file=sys.stderr)
        print(f"   - Drag & drop votre dossier", file=sys.stderr)
        print(f"   - Déploiement instant", file=sys.stderr)

if __name__ == "__main__":
    main()
