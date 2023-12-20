package main

import (
	"crypto/tls"
	"crypto/x509"
	"fmt"
	"io"
	"io/ioutil"
	"net"
	"os"
	"os/signal"
	"strings"
	"syscall"
	"time"
)

func main() {
	certificatePath := os.Getenv("CERTIFICATE_PATH")
	keyPath := os.Getenv("KEY_PATH")
	caPath := os.Getenv("CA_CERTIFICATE_PATH")
	remoteHost := os.Getenv("REMOTE_HOST")

	if certificatePath == "" || keyPath == "" || caPath == "" || remoteHost == "" {
		fmt.Println("ERROR: all required environment variables must be set.")
		os.Exit(1)
	}

	fmt.Printf("CERTIFICATE_PATH=%s\n", certificatePath)
	fmt.Printf("KEY_PATH=%s\n", keyPath)
	fmt.Printf("CA_PATH=%s\n", caPath)
	fmt.Printf("REMOTE_HOST=%s\n", remoteHost)

	cert, err := tls.LoadX509KeyPair(certificatePath, keyPath)
	if err != nil {
		fmt.Printf("Failed to load key pair: %v\n", err)
		os.Exit(1)
	}

	caCert, err := ioutil.ReadFile(caPath)
	if err != nil {
		fmt.Printf("Failed to read CA certificate: %v\n", err)
		os.Exit(1)
	}

	caCertPool := x509.NewCertPool()
	caCertPool.AppendCertsFromPEM(caCert)

	tlsConfig := &tls.Config{
		Certificates: []tls.Certificate{cert},
		RootCAs:      caCertPool,
		ServerName:   remoteHost,
	}

	serverPorts := []string{"9000" /*, "9001", "18510" */}
	fmt.Println("Connecting on ports: " + strings.Join(serverPorts, ", "))

	for _, port := range serverPorts {
		go tlsConnectAndSendPeriodically(remoteHost, port, tlsConfig)
	}

	// Handle SIGTERM for graceful shutdown
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGTERM)
	<-sigChan
	fmt.Println("Shutting down gracefully")
}

func tlsConnectAndSendPeriodically(host, port string, config *tls.Config) {
	address := net.JoinHostPort(host, port)
	conn, err := tls.Dial("tcp", address, config)
	if err != nil {
		fmt.Printf("Failed to connect: %v\n", err)
		return
	}
	defer conn.Close()

	fmt.Printf("Connected to %s\n", address)

	output := make(chan string)

	// Read stuff from the connection
	go func(output chan<- string) {
		for {
			buffer := make([]byte, 1024)
			n, err := conn.Read(buffer)
			if err != nil {
				if err != io.EOF {
					fmt.Printf("Error reading from connection: %v\n", err)
				}
				return
			}
			data := string(buffer[:n])
			fmt.Printf("Received from %s: %s\n", address, data)
		}
	}(output)

	// Write stuff periodically
	go func(output chan<- string) {
		for {
			message := fmt.Sprintf("Sending some data to port %s!", port)
			_, err := conn.Write([]byte(message))
			if err != nil {
				fmt.Printf("Error sending message: %v\n", err)
				return
			}
			fmt.Printf("Sent message to %s: %s\n", address, message)
			time.Sleep(2000 * time.Millisecond)
		}
	}(output)

	// Print stuff (Println doesn't lock so it becomes messy with several threads)
	go func(output <-chan string) {
		for {
			str := <-output
			fmt.Println(str)
		}
	}(output)

	shutdownChannel := make(chan os.Signal, 1)
	signal.Notify(shutdownChannel, syscall.SIGTERM, syscall.SIGINT)
	<-shutdownChannel
	fmt.Println("Exiting..")
}
