# Group 9 CommLab Final Project : Simulation of Arbitrated Quantum Signature Protocols

Group 9 Communication Lab Final Project
## Introduction 

The two files contain simulations for two AQS schemes. One uses the chained CNOT encryption method [[1]](#1) while the other applies quantum one time pad encryption[[2]](#2). The schemes are based on the referenced papers. 

## General

* **QKD protocol** : the quantum signature is built on a QKD protocol. The protocol ensures the security of the shared keys between Alice, Trent and Bob, Trent. The generated random string is also passed through a randomness test to ensure the randomness of the string.

For both protocols, Alice acts as the signatory, Bob as the receiver and Trent as the arbitrator. The protocols can be divided into 4 phases each : 

* **Initializing Phase** : Prepares and distributes QKD keys **K_AT, K_BT** and Entangled Bell states **create_bell_states** for Alice and Bob. Alice generates message **P**. Usually more than one copy of the message will be created. 

* **Signing Phase** : Alice creates her signature using encryption methods(chained CNOT or QOTP). Alice also performs bell measurement on her message bit and her entangled Bell State.

* **Verification Phase** : Bob will verify the authenticity of Alice's signature with Trent's assistance. With Alice's bell state measurement results, Bob can get Alice's message through calculation.

* **Dispute Resolving Phase** : When a dispute occurs between Alice and Bob, Bob will have to send the signature, message pair to Trent for dispute handling.

## Encryption Methods

* **QOTP Encryption** : QOTP encryption method applies Pauli-x to a qubit when key[2\*i] = 1, and Pauli-z when key[2\*i+1] = 1. 

![alt text](images/qotp.png?raw=true)

* **Chained-CNOT Encryption** : Chained-CNOT encryption encrypts creates n/2 pairs of control-target pairs based on the encryption key using the CNOT gate. 

![alt text](images/chained_cnot_encryption.png?raw=true)

## State Comparison

* **SWAP test** : multiple qubit SWAP test is used for state comparison. This allows us to check if 2 multiple qubits states are identical or not. Each test requires one ancilla bit.

![alt text](images/swaptest.png?raw=true)

## Security Test

To discriminate the security risk between using QOTP encryption and Chained-CNOT encryption, we chose Bob's forgery attack[[3]](#3). Since Bob already has a (P, S) pair from Alice, this is called a known message attack. 

Results show that with the chained-CNOT encryption method, Bob's forgery will not pass Trent's dispute handling. On the other hand, Bob can easily perform known message attack on QOTP encryption schemes.

## References

<a id=1>[1]</a> Q. Li, et al. “Arbitrated quantum signature scheme using Bell states,” Physical Review A, vol. 79, no. 5, 2009, p. 054307.

<a id=2>[2]</a> Li, Feng-Guang, and Jian-Hong Shi. "An arbitrated quantum signature protocol based on the chained CNOT operations encryption." Quantum Information Processing 14.6 (2015): 2171-2181.

<a id=3>[3]</a> Gao, Fei, et al. "Cryptanalysis of the arbitrated quantum signature protocols." Physical Review A 84.2 (2011): 022344.
