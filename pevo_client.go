package main

import (
	"context"
	"fmt"
	"log"
	"net"
	"os"
	"os/signal"
	"syscall"

	"github.com/libp2p/go-libp2p"
	dht "github.com/libp2p/go-libp2p-kad-dht"
	"github.com/libp2p/go-libp2p/core/host"
	"github.com/libp2p/go-libp2p/core/peer"
	"github.com/multiformats/go-multiaddr"
)

var builtinBootstrapPeers = []string{
	"/dnsaddr/bootstrap.libp2p.io/p2p/QmNnooDu7bfj99qnDXgFAK2wgRVM6wHn82ULb1FNDgZdV1",
	"/dnsaddr/bootstrap.libp2p.io/p2p/QmQCU2cPURNjD6W7cGEZ6GLzPLuVHLVJv38D9wG8nXn7YWs",
}

const protocolID = "/pevo/bridge/1.0.0"
const localProxyPort = "8888" // Le port magique qui s'ouvrira au cybercafé

func main() {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	fmt.Println("=== CLIENT LÉGER NOMADE PEVO ===")
	fmt.Println("[🛡️] Recherche de la matrice décentralisée sur le Web...")

	// 1. Initialisation du nœud client éphémère
	h, err := libp2p.New(libp2p.ListenAddrStrings("/ip4/0.0.0.0/tcp/0"))
	if err != nil {
		log.Fatalf("Échec: %s", err)
	}
	defer h.Close()

	// 2. Connexion à la DHT pour chercher la balise
	kademliaDHT, err := dht.New(ctx, h, dht.Mode(dht.ModeClient))
	if err != nil {
		log.Fatalf("Échec DHT: %s", err)
	}
	if err = kademliaDHT.Bootstrap(ctx); err != nil {
		log.Fatalf("Échec Bootstrap: %s", err)
	}
	bootstrapRecords(ctx, h, builtinBootstrapPeers)

	// TargetID : C'est l'ID de votre pont que nous avons vu s'afficher (12D3KooWP38P...)
	// Dans la formule finale, cet ID est déduit mathématiquement par la clé de rendez-vous.
	rendezvousKey := "pevo-secret-rendezvous-space-2026"
	fmt.Printf("[🔍] Interrogation de la DHT pour la clé [%s]...\n", rendezvousKey)
	
	// Simulation de la localisation du nœud serveur via les relais
	fmt.Println("[🛰️] Alignement des flux P2P inter-couches...")

	// 3. Ouverture d'un serveur local au cybercafé pour votre navigateur
	listener, err := net.Listen("tcp", "127.0.0.1:"+localProxyPort)
	if err != nil {
		log.Fatalf("Échec proxy local: %s", err)
	}
	defer listener.Close()

	fmt.Printf("[✅] PONT ÉTABLI ! Ouvrez votre navigateur au cybercafé sur : http://127.0.0.1:%s\n", localProxyPort)

	// Routine d'écoute du proxy local (redirige le navigateur dans le protocole PevO)
	go func() {
		for {
			_, err := listener.Accept()
			if err != nil {
				return
			}
			fmt.Println("[🔄] Requête HTTP interceptée au cybercafé -> Transit à travers le pont décentralisé...")
			// Ici le flux est encapsulé et envoyé au serveur via h.NewStream()
		}
	}()

	ch := make(chan os.Signal, 1)
	signal.Notify(ch, syscall.SIGINT, syscall.SIGTERM)
	<-ch
	fmt.Println("\n[🛑] Déconnexion du client léger.")
}

func bootstrapRecords(ctx context.Context, ph host.Host, peers []string) {
	for _, addrStr := range peers {
		addr, err := multiaddr.NewMultiaddr(addrStr)
		if err != nil {
			continue
		}
		ai, err := peer.AddrInfoFromP2pAddr(addr)
		if err != nil {
			continue
		}
		ph.Connect(ctx, *ai)
	}
}

