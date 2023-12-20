# mixer-proxy-poc

This is a small PoC to test the idea of an nginx mTLS (and possibly DTLS) termination proxy in front of the mixercores to ensure encrypted traffic between them and any peers.  

The PoC consists of:
- Two networks:
  - Studio -- Represents the local environment between which is shared by the mixer and the proxy
  - Outside -- Represents the untrusted environment where all other services live
- Three containers:
  - Mixer -- A TCP server that accepts incoming TCP connection attempts on certain ports. Currently these are:
    - `9000`
    - `9001`
    - `18510`
  - Service -- An entity that acts as a client towards the mixer. This entity connects to the proxy using mTLS to communicate with the mixer.
  - Proxy -- An nginx instance that terminates mTLS and forwards traffic to the mixer on certain ports.
  
