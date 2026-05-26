# PevO - Architecture Polyglotte Alignée

## Formule Centrale

```
P(t) = Σ αᵢ · Sᵢ(t) · Fᵢ(t)
P(t) = α₁·S₁(t)·F₁(t) + α₂·S₂(t)·F₂(t) + α₃·S₃(t)·F₃(t)
```

### Paramètres

- **αᵢ** : Coefficients de pondération par couche
  - α₁ = 0.40 (Surface)
  - α₂ = 0.35 (Deep)
  - α₃ = 0.25 (Darknet)

- **Sᵢ(t)** : Sécurité dynamique par couche
  - S₁(t) = 0.95 (Surface - locale, calculée en Python)
  - S₂(t) = 0.85 (Deep - réseau, interrogée via nœud Go)
  - S₃(t) = dynamique (Darknet - interrogée via nœud Rust)

- **Fᵢ(t)** : Fiabilité progressive par couche
  - F₁(t) = 0.99 (Surface - prédéfinie)
  - F₂(t) = 0.90 (Deep - calculée via consensus réseau)
  - F₃(t) = 0.60 (Darknet - prédéfinie)

- **C(t)** : Facteur cognitif
  - Nominal: C(t) = 1.0
  - Sous perturbation: C(t) = 1.45

## Architecture Polyglotte

```
~/pevo/
├── pevo.py                      ← Orchestrateur Cognitif (Python)
│                                  Rôle: Coordination, IA, formule centrale
│                                  Port: 8080 (hébergement web)
│
├── nodes/
│   ├── darknet_node/
│   │   ├── src/main.rs          ← Sécurité Bas Niveau (Rust)
│   │   │                          Rôle: Calcul S₃(t), chiffrement bas niveau
│   │   │                          Port: 8081 (TCP serveur)
│   │   └── Cargo.toml
│   │
│   └── deep_node/
│       ├── main.go              ← Fiabilité Réseau (Go)
│       │                         Rôle: Consensus blockchain, calcul F₂(t)
│       │                         Port: 8082 (TCP serveur)
│       └── go.mod
│
└── core/                        ← Utilitaires transversaux
    ├── __init__.py
    └── crypto.py               ← Chiffrement XOR partagé

```

## Rôles Spécialisés

### Python - Orchestrateur Cognitif
- Applique la formule P(t)
- Coordonne les trois couches
- Ajuste les facteurs en temps réel (C(t), α)
- Héberge l'interface web (port 8080)
- Chiffre/déchiffre avec XOR (clé 0x42)

### Rust - Sécurité Bas Niveau
- Calcule S₃(t) : sécurité dynamique
- Utilise: `S(t) = (e^(-λ·t/q) + β)^q`
- Performance critique en calcul sécurisé
- Serveur TCP persistant (port 8081)

### Go - Fiabilité Réseau
- Calcule F₂(t) : fiabilité progressive
- Valide consensus blockchain (registre en chaîne)
- Distribution efficace et goroutines
- Serveur TCP persistant (port 8082)

## Flux d'Exécution

1. **Initialisation**
   - Python crée OrchestrateurCognitif
   - Lance serveur HTTP (8080)
   - Démarre la boucle d'écoute

2. **Calcul de P(t)**
   - Python interroge Rust (8081): obtient S₃(t)
   - Python interroge Go (8082): obtient F₂(t)
   - Python calcule: P(t) = Σ αᵢ · Sᵢ(t) · Fᵢ(t)

3. **Adaptation IA**
   - Monitore les performances
   - Ajuste C(t) et α en cas de perturbation
   - Rééquilibre les couches

## Chiffrement

Tous les échanges TCP utilisent XOR avec clé `0x42`:
- Requête Python → Rust/Go (chiffrée)
- Réponse Rust/Go → Python (chiffrée)

## Compilation et Démarrage

```bash
# Compiler Rust
cd nodes/darknet_node && cargo build --release

# Compiler Go
cd nodes/deep_node && go build -o deep_node

# Démarrer l'orchestrateur Python
python3 pevo.py
```

## État Nominal

```
[Python] Orchestrateur actif sur http://localhost:8080
[RUST] Nœud Darknet (Sécurité Bas Niveau) en écoute sur 127.0.0.1:8081...
[GO] Nœud Deep (Fiabilité Progressive) en écoute sur 127.0.0.1:8082...
[PevO] P(t) = 0.8652 (valeur estimée)
```
