from os import name
from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from numpy.random import randint
import numpy as np
import math

# randomness test
def runsTest(l, l_median):

    runs, n1, n2 = 0, 0, 0

    # Checking for start of new run
    for i in range(len(l)):

        # no. of runs
        if (l[i] >= l_median and l[i-1] < l_median) or \
                (l[i] < l_median and l[i-1] >= l_median):
            runs += 1

        # no. of positive values
        if(l[i]) >= l_median:
            n1 += 1

        # no. of negative values
        else:
            n2 += 1

    runs_exp = ((2*n1*n2)/(n1+n2))+1
    stan_dev = math.sqrt((2*n1*n2*(2*n1*n2-n1-n2))/ \
                    (((n1+n2)**2)*(n1+n2-1)))
    z = (runs-runs_exp)/stan_dev
    return z

def encode_message(bits, bases):
    n = len(bits)
    message = []
    for i in range(n):
        qc = QuantumCircuit(1,1)
        if bases[i] == 0: # Prepare qubit in Z-basis
            if bits[i] == 0:
                pass 
            else:
                qc.x(0)
        else: # Prepare qubit in X-basis
            if bits[i] == 0:
                qc.h(0)
            else:
                qc.x(0)
                qc.h(0)
        qc.barrier()
        message.append(qc)
    return message

def measure_message(message, bases):
    n = len(bases)
    backend = Aer.get_backend('aer_simulator')
    measurements = []
    for q in range(n):
        if bases[q] == 0: # measuring in Z-basis
            message[q].measure(0,0)
        if bases[q] == 1: # measuring in X-basis
            message[q].h(0)
            message[q].measure(0,0)
        aer_sim = Aer.get_backend('aer_simulator')
        qobj = assemble(message[q], shots=1, memory=True)
        result = aer_sim.run(qobj).result()
        measured_bit = int(result.get_memory()[0])
        measurements.append(measured_bit)
    return measurements

def remove_garbage(a_bases, b_bases, bits):
    n = len(a_bases)
    good_bits = []
    for q in range(n):
        if a_bases[q] == b_bases[q]:
            good_bits.append(bits[q])
    return good_bits

def sample_bits(bits, selection):
    sample = []
    for i in selection:
        i = np.mod(i, len(bits))
        sample.append(bits.pop(i))
    return sample

# main function
def QKD(key_len):
    # generate random key for Alice
    n = key_len*5
    # check if bits are random enough
    flag = 0
    while flag == 0:
        alice_bits = randint(2,size=n)
        alice_bases = randint(2,size=n)
        Z1 = abs(runsTest(alice_bits, 0.5))
        Z2 = abs(runsTest(alice_bases, 0.5))
        if (Z1<1.96) and (Z2<1.96): # confidence level of 95%
            flag = 1
            #print('pass random test!')
    # encode it into quantum bits
    message = encode_message(alice_bits, alice_bases)
    
    # teleport to Bob 
    bob_bases = randint(2, size=n)
    bob_results = measure_message(message, bob_bases)
    
    # Bob announce his bases
    # Alice announce her bases
    
    # Alice remove bits whose bases are different from Bob
    alice_key = remove_garbage(alice_bases, bob_bases, alice_bits)
    # Bob remove bits whose bases are different from Alice
    bob_key = remove_garbage(alice_bases, bob_bases, bob_results)
    
    # select useful bits for key
    bit_selection = randint(n, size=key_len)
    bob_sample = sample_bits(bob_key, bit_selection)
    alice_sample = sample_bits(alice_key, bit_selection)
    
    # check if eve exists
    if bob_sample == alice_sample:
        return alice_sample
    else:
        raise ExampleError("key has been intercepted!!!")

if __name__ == "__main__": 
    key = QKD(20)
    print(key)
