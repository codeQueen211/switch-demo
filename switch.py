import sys
import random
import numpy  as np

class Switch:
    def  __init__(self, T, N, M, Q, P, Lambdas, mus):
        self.T=T
        self.q=Q #size of queue for each output m 
        self.num_input=N
        self.num_output=M
        self.P=P #probabilty matrix for routing a package 
        self.Lambdas=Lambdas #frequency of package arrival at entry
        self.mus=mus # frequency of transmission for each outout port
        print("Initialized Switch with:", T, N, M, Q, P, Lambdas, mus)
        self.time = 0
        self.arrivals = np.zeros(N)  # Keeps track of arrival times for each input port
        self.queues = [[] for _ in range(M)]  # Queues for each output port
    
    # y- number of packages successfully routed, happens in two cases:
    #1) if the port queue is empty  and there are no other packets waiting to be sent
    #2) if there are packets in the port queue but it's not full 
    
    def simulate(self):
        #simulation logic here
         print("Type of self.P:", type(self.P))
         Y=0
         y_i=[0]* self.num_output  # Initialize y_i with zeros for each output port
         X=0
         x_i=[0]* self.num_output  # Initialize x_i with zeros for each output port
         finish_time = 0
         while self.time < self.T:
            # Simulate arrivals at input ports
            for i in range(self.num_input):
                if random.random() < self.Lambdas[i]:
                    self.arrivals[i] = self.time

            # Attempt to route arrived packets to output ports
            for i in range(self.num_input):
                # print("Value of i:", i) 
                for j in range(self.num_output-1):
                    #   print("Value of j:", j)
                    #   print("Length of self.P:", len(self.P))
                    #   print("length of q:", len(self.q[j]))
                    #   if random.random() < self.P[i][j]:
                      if len(self.queues[j]) < len(self.q[j]):  # If output port is not full
                            self.queues[j].append((i, self.time))  # Enqueue the packet
                            Y+=1 
                            y_i[j]+=1
                      else:
                            # Discard the packet if the queue is full
                            #here we need to return x packets discarded 
                            #keep track of each x_i a packet that was sent to output i and was discarded
                            x_i[j]+=1 
                            X+=1 
                            pass

            # Transmit packets from queues to output ports
            for j in range(self.num_output):
                if self.queues[j]:
                    transmit_count = np.random.poisson(self.mus[j])
                    transmitted_packets = self.queues[j][:transmit_count]
                    self.queues[j] = self.queues[j][transmit_count:]
                  
                    
            # Update simulation time
         self.time += 1
         finish_time = self.time
        # Print or return the calculated values
         print("Y:", Y)
         print("y_i:", y_i)
         print("X:", X)
         print("x_i:", x_i)
         print("Finish time:", finish_time)
       
         pass
    
def parse_input(argv):
    T = int(argv[1])
    N = int(argv[2])
    M = int(argv[3])
    
    # Initialize an empty list for P
    P = []
     # Parse the flat list of probabilities into a 2D list
    start_index = 4
    for i in range(N):
        row = [(argv[start_index + i * M + j]) for j in range(M)]
        P.append(row)
    lambdas = [float(argv[4 + N*M + i]) for i in range(N)]
    Q = [int(argv[4 + N*M +N+ i]) for i in range(M)]
    mus = [float(argv[4 + N*M + M +N+ i]) for i in range(M)]
    print("P:", P)  # Print the constructed P
    print("N:", N)
    print("M:", M)
    print('lambdas:', lambdas)
    print('Q:', Q)
    print('mus:', mus)
    print("Parsed arguments:", T, N, M, P, lambdas, Q, mus)
    return T, N, M, P, lambdas, Q, mus
  
   


def main(argv):
    print("Command-line arguments:", argv)
    if len(argv) != (3 + int(argv[2]) * int(argv[3]) + int(argv[2]) + 2 * int(argv[3])+1):

        print("Invalid number of arguments.")
        print("Usage: python script.py T N M P00 P01 ... P(N-1)(M-1) lambda0 lambda1 ... lambda(N-1) Q0 Q1 ... Q(M-1) mu0 mu1 ... mu(M-1)")
        return
    
   # Parse command-line arguments
    T, N, M, P, lambdas, Q, mus = parse_input(argv)

    # Initialize Switch and simulate
    switch_simulator = Switch(T, N, M, P, lambdas, Q, mus)
    switch_simulator.simulate()

if __name__ == "__main__":
    main(sys.argv)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    