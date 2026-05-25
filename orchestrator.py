import os
import sys
import subprocess
import time

HOSTED_DIR = os.path.expanduser("~/PevO/hosted_sites")

def init_pevo_space():
    print("=== ORCHESTRATEUR DE COUCHE PEVO ===")
    print("[🛡️] Formule de sécurité évolutive active : Mode Hébergement On-Demand.")
    if not os.path.exists(HOSTED_DIR):
        os.makedirs(HOSTED_DIR)

def deploy_site_on_demand(site_name, port):
    """
    Isole et héberge un site web à la demande dans un conteneur éphémère Nginx
    qui servira de point d'entrée pour notre pont inter-couches.
    """
    site_path = os.path.join(HOSTED_DIR, site_name)
    
    # Création d'une page d'accueil par défaut si le dossier est vide
    if not os.path.exists(site_path):
        os.makedirs(site_path)
        with open(os.path.join(site_path, "index.html"), "w") as f:
            f.write(f"<html><body style='background:#0d1117;color:#58a6ff;font-family:sans-serif;text-align:center;padding-top:10%;'>")
            f.write(f"<h1>[PevO Hub] Site autonome : {site_name}</h1>")
            f.write(f"<p>Statut : Actif et protégé par la matrice évolutive.</p>")
            f.write(f"</body></html>")

    print(f"[🏠] Initialisation de l'espace pour '{site_name}'...")

    # Commande Docker pour lancer un serveur Nginx ultra-léger et isolé pour ce site spécifique
    container_name = f"pevo_site_{site_name}"
    
    # On nettoie une éventuelle ancienne instance du même nom
    subprocess.run(f"sudo docker stop {container_name} >/dev/null 2>&1", shell=True)
    
    docker_cmd = (
        f"sudo docker run --rm -d "
        f"-v {site_path}:/usr/share/nginx/html:ro "
        f"-p {port}:80 "
        f"--name {container_name} "
        f"nginx:alpine"
    )
    
    subprocess.run(docker_cmd, shell=True)
    print(f"[✅] Site déployé avec succès en isolation complète.")
    print(f"[🌐] Liaison Pont active : Accessible localement sur le port {port} pour acheminement DHT.")

if __name__ == "__main__":
    init_pevo_space()
    
    # Test de déploiement à la demande d'un premier site autonome nommé "projet_omega" sur le port 9090
    deploy_site_on_demand("projet_omega", 9090)

