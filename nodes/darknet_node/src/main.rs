use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    
    // Vérification des arguments pour garantir l'absence de crash (anti-Signal 9)
    if args.len() < 5 {
        eprintln!("Usage: darknet_node <t> <lambda> <beta> <Q>");
        std::process::exit(1);
    }

    // Extraction et parsing des paramètres de sécurité dynamique
    let t: f64 = args[1].parse().unwrap_or(0.0);
    let lambda_base: f64 = args[2].parse().unwrap_or(0.1);
    let beta: f64 = args[3].parse().unwrap_or(0.5);
    let q: f64 = args[4].parse().unwrap_or(1.1);

    // MATÉRIALISATION DU FACTEUR QUANTIQUE (Q) :
    // L'intrication et la distribution de clés (QKD) réduisent l'impact des failles.
    // Plus Q est élevé, plus le taux de dégradation effectif diminue : lambda_effectif = lambda_base / Q
    let lambda_effectif = lambda_base / q;

    // Calcul de la sécurité dynamique : S_i(t) = e^(-lambda_effectif * t) + beta
    let s_i_t = (-lambda_effectif * t).exp() + beta;

    // Application de l'exposant quantique final : S_futur = S_i(t) ^ Q
    let s_futur = s_i_t.powf(q);

    // Borner mathématiquement le résultat entre 0.0 et 1.0 pour la cohérence probabiliste
    let s_futur_borne = s_futur.min(1.0).max(0.0);

    // Sortie brute lue par l'orchestrateur Python
    println!("{:.4}", s_futur_borne);
}
