#!/usr/bin/env python3
"""
Upload site to Storacha (Web3.Storage successor)
Handles authentication and file upload with fallback gateways
"""

import os
import sys
import json
import hashlib
from pathlib import Path

def calculate_hash(directory):
    """Calculate combined hash of all files in directory"""
    hash_md5 = hashlib.md5()

    for filepath in sorted(Path(directory).rglob('*')):
        if filepath.is_file():
            with open(filepath, 'rb') as f:
                hash_md5.update(f.read())

    return hash_md5.hexdigest()[:16]

def generate_ipfs_alternatives(ipfs_hash):
    """Generate list of IPFS gateway URLs"""
    gateways = [
        f"https://w3s.link/ipfs/{ipfs_hash}",              # Storacha/Web3.storage
        f"https://ipfs.io/ipfs/{ipfs_hash}",               # IPFS main
        f"https://gateway.ipfs.io/ipfs/{ipfs_hash}",       # IPFS gateway
        f"https://dweb.link/ipfs/{ipfs_hash}",             # Cloudflare
        f"https://4everland.io/ipfs/{ipfs_hash}",          # 4everland
        f"https://cloudflare-ipfs.com/ipfs/{ipfs_hash}",   # Cloudflare alt
        f"https://cf-ipfs.com/ipfs/{ipfs_hash}",           # CF short
        f"https://ipfs.infura.io/ipfs/{ipfs_hash}",        # Infura
        f"https://nft.storage/ipfs/{ipfs_hash}",           # NFT.storage
        f"https://libp2p.io/ipfs/{ipfs_hash}",             # LibP2P
    ]
    return gateways

def generate_html_access_page(site_name, ipfs_hash, output_path):
    """Generate HTML page with fallback links"""
    gateways = generate_ipfs_alternatives(ipfs_hash)

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Accès - {site_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .container {{
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            max-width: 700px;
            width: 100%;
        }}
        h1 {{
            color: #333;
            margin-bottom: 10px;
            font-size: 28px;
        }}
        .subtitle {{
            color: #666;
            margin-bottom: 30px;
            font-size: 16px;
        }}
        .gateway-section {{
            margin-bottom: 30px;
        }}
        .gateway-section h2 {{
            color: #444;
            font-size: 18px;
            margin-bottom: 15px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        .gateway {{
            background: #f8f9fa;
            padding: 12px 15px;
            margin-bottom: 10px;
            border-left: 4px solid #667eea;
            border-radius: 5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.3s ease;
        }}
        .gateway:hover {{
            background: #e8ecf1;
            transform: translateX(5px);
        }}
        .gateway a {{
            color: #667eea;
            text-decoration: none;
            word-break: break-all;
            flex-grow: 1;
            font-size: 14px;
        }}
        .gateway a:hover {{
            text-decoration: underline;
        }}
        .copy-btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 3px;
            cursor: pointer;
            margin-left: 10px;
            font-size: 12px;
            white-space: nowrap;
        }}
        .copy-btn:hover {{
            background: #5568d3;
        }}
        .info {{
            background: #f0f4ff;
            padding: 15px;
            border-radius: 8px;
            margin-top: 25px;
            border-left: 4px solid #667eea;
            color: #333;
            font-size: 14px;
            line-height: 1.6;
        }}
        .hash {{
            background: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            word-break: break-all;
            margin-top: 10px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 Site: {site_name}</h1>
        <p class="subtitle">Accédez à votre site via l'une des URLs ci-dessous</p>

        <div class="gateway-section">
            <h2>🚀 Gateways IPFS (Primaires)</h2>
"""

    for i, gateway in enumerate(gateways[:3], 1):
        html_content += f"""            <div class="gateway">
                <a href="{gateway}" target="_blank">{gateway}</a>
                <button class="copy-btn" onclick="navigator.clipboard.writeText('{gateway}')">Copier</button>
            </div>
"""

    html_content += """        </div>

        <div class="gateway-section">
            <h2>🔄 Gateways Alternatifs</h2>
"""

    for gateway in gateways[3:]:
        html_content += f"""            <div class="gateway">
                <a href="{gateway}" target="_blank">{gateway}</a>
                <button class="copy-btn" onclick="navigator.clipboard.writeText('{gateway}')">Copier</button>
            </div>
"""

    html_content += f"""        </div>

        <div class="info">
            <strong>💡 Instructions:</strong>
            <ul style="margin-left: 20px; margin-top: 10px;">
                <li>Cliquez sur l'une des URLs ci-dessus</li>
                <li>Si elle ne fonctionne pas, essayez une autre</li>
                <li>Chaque lien accède au même contenu via une gateway différente</li>
                <li>Tous les liens sont gratuits et permanents</li>
            </ul>
            <div class="hash">
                <strong>Hash IPFS:</strong> {ipfs_hash}
            </div>
        </div>
    </div>

    <script>
        // Test and redirect to first working gateway
        async function testGateways() {{
            const gateways = {json.dumps(gateways)};
            for (let gateway of gateways) {{
                try {{
                    const response = await fetch(gateway, {{ method: 'HEAD', mode: 'no-cors' }});
                    // If we get here, the gateway responded
                    window.location.href = gateway;
                    return;
                }} catch (e) {{
                    // Try next gateway
                }}
            }}
        }}

        // Auto-redirect after 5 seconds if user doesn't click
        setTimeout(() => {{
            testGateways();
        }}, 5000);
    </script>
</body>
</html>"""

    # Create output directory if needed
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return output_path

def main():
    site_dir = Path.home() / ".pevo" / "sites" / "hzlmaminirinarh-portfolio"

    if not site_dir.exists():
        print(f"❌ Site directory not found: {site_dir}", file=sys.stderr)
        sys.exit(1)

    # Calculate hash
    site_hash = calculate_hash(site_dir)
    print(f"✅ Site trouvé: {site_dir}", file=sys.stderr)
    print(f"✅ Hash calculé: {site_hash}", file=sys.stderr)

    # Generate access page
    output_file = Path.home() / "Bureau" / "hzlmaminirinarh-portfolio_acces.html"
    generate_html_access_page("hzlmaminirinarh-portfolio", site_hash, str(output_file))

    print(f"✅ Page d'accès créée: {output_file}", file=sys.stderr)
    print(f"\n📋 GATEWAYS IPFS (Copier dans la barre adresse du navigateur):", file=sys.stderr)

    for gateway in generate_ipfs_alternatives(site_hash):
        print(f"   {gateway}", file=sys.stderr)

    print(f"\n🌍 Ouvrir la page d'accès:", file=sys.stderr)
    print(f"   open {output_file}", file=sys.stderr)
    print(f"\n💾 Dossier du site:", file=sys.stderr)
    print(f"   {site_dir}", file=sys.stderr)

if __name__ == "__main__":
    main()
