import (
	"fmt"
	"math"
	"os"
	"strconv"
)

// Structure émulant un bloc de registre pour valider l'état d'une couche réseau
type BlocConsensus struct {
	Index        int
	NomCouche    string
	Fiabilite    float64
	HashPrecedent string
	Hash         string
}

// Calcule un hash SHA-256 pour garantir l'immuabilité du consensus
func calculerHash(b BlocConsensus) string {
	enregistrement := strconv.Itoa(b.Index) + b.NomCouche + fmt.Sprintf("%.4f", b.Fiabilite) + b.HashPrecedent
	h := sha256.New()
	h.Write([]byte(enregistrement))
	return fmt.Sprintf("%x", h.Sum(nil))
}

func main() {
	// Arguments : <fiabilite_base> <facteur_B> <nom_couche>
	if len(os.Args) < 4 {
		fmt.Println("Usage: deep_node <fiabilite_base> <facteur_b> <nom_couche>")
		os.Exit(1)
	}

	fiabiliteBase, _ := strconv.ParseFloat(os.Args[1], 64)
	bFactor, _ := strconv.ParseFloat(os.Args[2], 64)
	nomCouche := os.Args[3]

	// 1. SIMULATION DU REGISTRE DISTRIBUÉ ET PROTOCOLE DE CONSENSUS (Facteur B)
	// On crée un bloc de genèse et un bloc de transaction pour valider la route réseau
	blocGenese := BlocConsensus{Index: 0, NomCouche: "Genesis", Fiabilite: 1.0, HashPrecedent: "0"}
	blocGenese.Hash = calculerHash(blocGenese)

	blocValidation := BlocConsensus{
		Index:         1,
		NomCouche:     nomCouche,
		Fiabilite:     fiabiliteBase,
		HashPrecedent: blocGenese.Hash,
	}
	blocValidation.Hash = calculerHash(blocValidation)

	// Vérification de l'intégrité du hash (Simule le consensus des validateurs)
	consensusValide := true
	if blocValidation.HashPrecedent != blocGenese.Hash {
		consensusValide = false
	}

	// 2. APPLICATION DU FACTEUR BLOCKCHAIN SUR LA FIABILITÉ (F_futur)
	var fiabiliteFutur float64
	if consensusValide {
		// Le consensus est validé : la fiabilité cumulative s'applique à son plein potentiel
		// On applique une atténuation de la surcharge réseau grâce à la redondance du consensus
		// F_futur = fiabiliteBase ^ (1 / bFactor) si bFactor optimise, ou fiabiliteBase ^ bFactor selon la charge
		// Pour coller à l'équation théorique : F_i(t)^B
		// Si le consensus est fort, il stabilise la structure face au facteur de surcharge (mu)
                   fiabiliteFutur = math.Pow(fiabiliteBase, bFactor)

	} else {
		// Échec du consensus / Altération détectée : effondrement de la fiabilité
		fiabiliteFutur = 0.0
	}

	// Borner mathématiquement le coefficient entre 0.0 et 1.0
	if fiabiliteFutur > 1.0 {
		fiabiliteFutur = 1.0
	} else if fiabiliteFutur < 0.0 {
		fiabiliteFutur = 0.0
	}

	// Renvoie le résultat lu par Python
	fmt.Printf("%.4f\n", fiabiliteFutur)
}

// Fonction de secours locale pour éviter d'importer math (réduction de l'empreinte mémoire anti-Signal 9)
func mathPow(base, exp float64) float64 {
	// Approximation rapide ou calcul via conversion si nécessaire. 
	// Go gère nativement les puissances via l'import "math", réintroduisons-le proprement :
	return purePow(base, exp)
}
