package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"net"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/libp2p/go-libp2p"
	dht "github.com/libp2p/go-libp2p-kad-dht"
	"github.com/libp2p/go-libp2p/core/host"
	"github.com/libp2p/go-libp2p/core/network"
	"github.com/libp2p/go-libp2p/core/peer"
	"github.com/multiformats/go-multiaddr"
)

var builtinBootstrapPeers = []string{
	"/dnsaddr/bootstrap.libp2p.io/p2p/QmNnooDu7bfj99qnDXgFAK2wgRVM6wHn82ULb1FNDgZdV1",
	"/dnsaddr/bootstrap.libp2p.io/p2p/QmQCU2cPURNjD6W7cGEZ6GLzPLuVHLVJv38D9wG8nXn7YWs",
}

// Protocole personnalisé PevO pour le transit inter-couches
const protocolID = "/pevo/bridge/1.0.0"
const targetLocalPort = "9090" // Le port de notre site hébergé à la demande

func main() {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	fmt.Println("=== MATRICE D'ANCRAGE & PONT MULTI-COUCHES PEVO ===")
	fmt.Println("[🛡️] Formule de sécurité évolutive : Activation du protocole de routage...")

	h, err := libp2p.New(
		libp2p.ListenAddrStrings("/ip4/0.0.0.0/tcp/0"),
	)
	if err != nil {
		log.Fatalf("Échec: %s", err)
	}
	defer h.Close()

	fmt.Printf("[ℹ️] ID Unique du Pont PevO : %s\n", h.ID().String())

	// CONFIGURATION DU PONT : On écoute les connexions entrantes sur notre protocole secret
	h.SetStreamHandler(protocolID, func(s network.Stream) {
		fmt.Println("[🔄] Connexion entrante via la DHT ! Redirection vers le site isolé...")
		
		// Connexion locale vers le conteneur Nginx (projet_omega sur le port 9090)
		localConn, err := net.Dial("tcp", "127.0.0.1:"+targetLocalPort)
		if err != nil {
			fmt.Printf("[❌] Impossible de joindre le site isolé : %s\n", err)
			s.Reset()
			return
		}
		defer localConn.Close()

		// Liaison bidirectionnelle des flux (Le Pont Transversal)
		go func() { _, _ = io.Copy(localConn, s) }()
		_, _ = io.Copy(s, localConn)
	})

	kademliaDHT, err := dht.New(ctx, h, dht.Mode(dht.ModeClient))
	if err != nil {
		log.Fatalf("Échec DHT: %s", err)
	}
	if err = kademliaDHT.Bootstrap(ctx); err != nil {
		log.Fatalf("Échec Bootstrap: %s", err)
	}

	bootstrapRecords(ctx, h, builtinBootstrapPeers)

	rendezvousKey := "pevo-secret-rendezvous-space-2026"
	go func() {
		for {
			fmt.Printf("[🔄] [%s] Balise active [%s] : En attente de requêtes inter-couches...\n", time.Now().Format("15:04:05"), rendezvousKey)
			time.Sleep(30 * time.Second)
		}
	}()

	ch := make(chan os.Signal, 1)
	signal.Notify(ch, syscall.SIGINT, syscall.SIGTERM)
	<-ch
	fmt.Println("\n[🛑] Fermeture du pont et de la matrice.")
}

func bootstrapRecords(ctx context.Context, ph host.Host, peers []string) {
	fmt.Println("[🌐] Amarrage aux instances dynamiques mondiales...")
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
	fmt.Println("[✅] Le pont est suspendu et prêt à relayer.")
}

