package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
)

func main() {
	if len(os.Args) < 3 {
		fmt.Println("Usage: deep_node <fiabilite_base> <facteur_b>")
		os.Exit(1)
	}

	fiabiliteBase, _ := strconv.ParseFloat(os.Args[1], 64)
	b, _ := strconv.ParseFloat(os.Args[2], 64)

	// Application du facteur Blockchain : F_futur = F_base ^ B
	fFutur := math.Pow(fiabiliteBase, b)

	// Renvoie le résultat brut sur la sortie standard
	fmt.Printf("%.4f\n", fFutur)
}
