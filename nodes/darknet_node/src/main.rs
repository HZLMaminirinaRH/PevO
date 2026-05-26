use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};

const XOR_KEY: u8 = 0x42;

fn dechiffrer_xor(donnees: &mut [u8]) {
    for byte in donnees.iter_mut() {
        *byte ^= XOR_KEY;
    }
}

fn chiffrer_xor(donnees: &mut Vec<u8>) {
    for byte in donnees.iter_mut() {
        *byte ^= XOR_KEY;
    }
}

fn calculer_securite_dynamique(t: f64, lambda: f64, beta: f64, q: f64) -> f64 {
    let lambda_effectif = lambda / q;
    let exponentielle = (-lambda_effectif * t).exp();
    let s_t = exponentielle + beta;
    let s_futur = s_t.powf(q);
    s_futur.min(1.0).max(0.0)
}

fn gerer_client(mut stream: TcpStream) {
    let mut buffer = [0; 512];

    if let Ok(bytes_lus) = stream.read(&mut buffer) {
        if bytes_lus == 0 {
            return;
        }

        let mut donnees_dechiffrees = buffer[..bytes_lus].to_vec();
        dechiffrer_xor(&mut donnees_dechiffrees);

        let requete_str = String::from_utf8_lossy(&donnees_dechiffrees);
        let parametres: Vec<&str> = requete_str.trim().split(',').collect();

        if parametres.len() >= 4 {
            let t = parametres[0].parse::<f64>().unwrap_or(0.0);
            let lambda_base = parametres[1].parse::<f64>().unwrap_or(0.1);
            let beta = parametres[2].parse::<f64>().unwrap_or(0.5);
            let q = parametres[3].parse::<f64>().unwrap_or(1.1);

            let s_dynamique = calculer_securite_dynamique(t, lambda_base, beta, q);

            let mut reponse = format!("{:.4}", s_dynamique).into_bytes();
            chiffrer_xor(&mut reponse);

            let _ = stream.write_all(&reponse);
            let _ = stream.flush();
        }
    }
}

fn main() {
    let adresse = "127.0.0.1:8081";
    let listener = TcpListener::bind(adresse).expect("Impossible de lier le port 8081");
    println!("[RUST] Nœud Darknet (Sécurité Bas Niveau) en écoute sur {}...", adresse);

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
