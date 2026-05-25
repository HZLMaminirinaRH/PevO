use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};

fn gerer_client(mut stream: TcpStream) {
    let mut buffer = [0; 512];
    
    // Lecture des données brutes envoyées par Python
    if let Ok(bytes_lus) = stream.read(&mut buffer) {
        if bytes_lus == 0 { return; }
        
        let requete_str = String::from_utf8_lossy(&buffer[..bytes_lus]);
        
        // Parsing manuel ultra-léger (évite d'importer la crate serde pour économiser la RAM de Termux)
        // Format attendu de Python : "t,lambda,beta,Q"
        let parametres: Vec<&str> = requete_str.trim().split(',').collect();
        
        if parametres.len() >= 4 {
            let t: f64 = parametres[0].parse().unwrap_or(0.0);
            let lambda_base: f64 = parametres[1].parse().unwrap_or(0.1);
            let beta: f64 = parametres[2].parse().unwrap_or(0.5);
            let q: f64 = parametres[3].parse().unwrap_or(1.1);

            // Matérialisation du Facteur Quantique (Immunité)
            let lambda_effectif = lambda_base / q;
            let s_i_t = (-lambda_effectif * t).exp() + beta;
            let s_futur = s_i_t.powf(q).min(1.0).max(0.0);

            // Préparation de la réponse textuelle brute
            let reponse = format!("{:.4}", s_futur);
            
            // Renvoi du résultat à travers le socket
            let _ = stream.write_all(reponse.as_bytes());
            let _ = stream.flush();
        }
    }
}

fn main() {
    let adresse = "127.0.0.1:8081";
    let listener = TcpListener::bind(adresse).expect("Impossible de lier le socket sur le port 8081");
    println!("[RUST] Nœud Darknet en écoute active sur {}...", adresse);

    // Boucle d'écoute continue (Serveur persistant)
    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                gerer_client(stream);
            }
            Err(e) => {
                eprintln!("[RUST] Erreur lors de la connexion : {}", e);
            }
        }
    }
}
