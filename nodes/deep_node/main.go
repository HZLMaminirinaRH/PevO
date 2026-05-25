package main

import (
	"crypto/sha256"
	"fmt"
	"math"
	"net"
	"os"
	"strconv"
	"strings"
        "net/http"
)

type BlocConsensus struct {
	Index         int
	NomCouche     string
	Fiabilite     float64
	HashPrecedent string
	Hash          string
}

func calculerHash(b BlocConsensus) string {
	enregistrement := strconv.Itoa(b.Index) + b.NomCouche + fmt.Sprintf("%.4f", b.Fiabilite) + b.HashPrecedent
	h := sha256.New()
	h.Write([]byte(enregistrement))
	return fmt.Sprintf("%x", h.Sum(nil))
}

func gererClient(conn net.Conn) {
	defer conn.Close()
	buffer := make([]byte, 512)

	bytesLus, err := conn.Read(buffer)
	if err != nil || bytesLus == 0 {
		return
	}

	// --- COUCHE SÉCURITÉ : Déchiffrement XOR avec la clé secrète 0x42 ---
	donneesDechiffrees := make([]byte, bytesLus)
	for i := 0; i < bytesLus; i++ {
		donneesDechiffrees[i] = buffer[i] ^ 0x42
	}

	requeteStr := string(donneesDechiffrees)
	parametres := strings.Split(strings.TrimSpace(requeteStr), ",")

	if len(parametres) >= 3 {
		fiabiliteBase, _ := strconv.ParseFloat(parametres[0], 64)
		bFactor, _ := strconv.ParseFloat(parametres[1], 64)
		nomCouche := parametres[2]

		// Simulation du Consensus du Registre
		blocGenese := BlocConsensus{Index: 0, NomCouche: "Genesis", Fiabilite: 1.0, HashPrecedent: "0"}
		blocGenese.Hash = calculerHash(blocGenese)

		blocValidation := BlocConsensus{
			Index:         1,
			NomCouche:     nomCouche,
			Fiabilite:     fiabiliteBase,
			HashPrecedent: blocGenese.Hash,
		}
		blocValidation.Hash = calculerHash(blocValidation)

		consensusValide := blocValidation.HashPrecedent == blocGenese.Hash

		var fiabiliteFutur float64
		if consensusValide {
			fiabiliteFutur = math.Pow(fiabiliteBase, bFactor)
		} else {
			fiabiliteFutur = 0.0
		}

		if fiabiliteFutur > 1.0 {
			fiabiliteFutur = 1.0
		} else if fiabiliteFutur < 0.0 {
			fiabiliteFutur = 0.0
		}

		reponseRaw := fmt.Sprintf("%.4f\n", fiabiliteFutur)
		reponseBytes := []byte(reponseRaw)

		// --- COUCHE SÉCURITÉ : Chiffrement XOR de la réponse ---
		for i := 0; i < len(reponseBytes); i++ {
			reponseBytes[i] ^= 0x42
		}

		conn.Write(reponseBytes)
	}
}

func main() {
	// Lancement du serveur d'hébergement Web autonome sur le port 8083
	go func() {
		fs := http.FileServer(http.Dir("../../www"))
		http.Handle("/", fs)
		fmt.Println("[GO] Serveur de stockage Web actif sur le port 8083...")
		if err := http.ListenAndServe("127.0.0.1:8083", nil); err != nil {
			fmt.Printf("[GO] Erreur serveur Web : %v\n", err)
		}
	}()

	// Le reste de votre fonction main() existante pour l'écoute TCP (Port 8082) reste inchangé
	adresse := "127.0.0.1:8082"
	listener, err := net.Listen("tcp", adresse)
	if err != nil {
		fmt.Printf("[GO] Erreur d'initialisation : %v\n", err)
		os.Exit(1)
	}
	defer listener.Close()
	fmt.Printf("[GO] Nœud Deep Web en écoute active sur %s...\n", adresse)

	for {
		conn, err := listener.Accept()
		if err != nil {
			continue
		}
		go gererClient(conn)
	}
}
