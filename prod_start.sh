#!/bin/bash

echo "======================================================="
echo "   PevO : Initialisation de l'Infrastructure Cloud"
echo "======================================================="

# 1. Nettoyage préventif des anciens processus
echo "[Système] Nettoyage des ports réseau..."
pkill -f darknet_node
pkill -f deep_node

# 2. Lancement des nœuds natifs en tâche de fond persistance
echo "[Système] Démarrage du Nœud Darknet (Rust) sur le port 8081..."
./nodes/darknet_node/target/release/darknet_node > /dev/null 2>&1 &

echo "[Système] Démarrage du Nœud Deep Web (Go) sur le port 8082..."
./nodes/deep_node/deep_node > /dev/null 2>&1 &

# Attente d'une seconde pour l'ouverture des sockets locales
sleep 1

# 3. Lancement de l'hébergeur et du moteur cognitif (Python)
echo "[Système] PevO est maintenant en ligne et accessible publiquement."
echo "--> Appuyez sur CTRL+C pour arrêter proprement le serveur."
python pevo.py
