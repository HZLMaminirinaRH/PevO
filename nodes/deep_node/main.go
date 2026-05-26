package main

import (
	"crypto/sha256"
	"fmt"
	"math"
	"net"
	"os"
	"strconv"
	"strings"
)

const XOR_KEY = 0x42

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

func dechiffrerXor(donnees []byte) []byte {
	for i := range donnees {
		donnees[i] ^= XOR_KEY
	}
	return donnees
}

func chiffrerXor(donnees []byte) []byte {
	for i := range donnees {
		donnees[i] ^= XOR_KEY
	}
	return donnees
}

func calculerFiabiliteProgressive(fiabBase, bFactor float64) float64 {
	fiabFutur := math.Pow(fiabBase, bFactor)
	if fiabFutur > 1.0 {
		return 1.0
	} else if fiabFutur < 0.0 {
		return 0.0
	}
	return fiabFutur
}

func gererClient(conn net.Conn) {
	defer conn.Close()
	buffer := make([]byte, 512)

	bytesLus, err := conn.Read(buffer)
	if err != nil || bytesLus == 0 {
		return
	}

	donneesDechiffrees := dechiffrerXor(buffer[:bytesLus])
	requeteStr := string(donneesDechiffrees)
	parametres := strings.Split(strings.TrimSpace(requeteStr), ",")

	if len(parametres) >= 3 {
		fiabiliteBase, _ := strconv.ParseFloat(parametres[0], 64)
		bFactor, _ := strconv.ParseFloat(parametres[1], 64)
		nomCouche := parametres[2]

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
			fiabiliteFutur = calculerFiabiliteProgressive(fiabiliteBase, bFactor)
		} else {
			fiabiliteFutur = 0.0
		}

		reponseRaw := fmt.Sprintf("%.4f\n", fiabiliteFutur)
		reponseBytes := []byte(reponseRaw)
		reponseBytes = chiffrerXor(reponseBytes)

		conn.Write(reponseBytes)
	}
}

func main() {
	adresse := "127.0.0.1:8082"
	listener, err := net.Listen("tcp", adresse)
	if err != nil {
		fmt.Printf("[GO] Erreur d'initialisation : %v\n", err)
		os.Exit(1)
	}
	defer listener.Close()
	fmt.Printf("[GO] Nœud Deep (Fiabilité Progressive) en écoute sur %s...\n", adresse)

	for {
		conn, err := listener.Accept()
		if err != nil {
			continue
		}
		go gererClient(conn)
	}
}
