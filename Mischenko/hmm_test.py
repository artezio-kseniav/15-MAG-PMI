import numpy as np
from hmmestimate import HMM
from copy import copy
import matplotlib.pyplot as plt

hmm = HMM()
hmm.pi = np.array([0.5, 0.5])
hmm.A = np.array([[0.85, 0.15],
                          [0.12, 0.88]])
hmm.B = np.array([[0.8, 0.1, 0.1],
                          [0.0, 0.0, 1]])
						  						  

												  
hmmguess = HMM()
        hmmguess.pi = np.array([0.5, 0.5])
        hmmguess.A = np.array([[0.5, 0.5],
                               [0.5, 0.5]])
        hmmguess.B = np.array([[0.3, 0.3, 0.4],
                               [0.2, 0.5, 0.3]])												  
o, s = hmm.simulate(10)

print(o, s)
hmmguess.train(o,0.0001,graphics=True)
print ('Actual probabilities\n', hmm.pi)
print ('Estimated initial probabilities\n', hmmguess.pi)

print ('Actual state transition probabililities\n', hmm.A)
print ('Estimated state transition probabililities\n',hmmguess.A)

print ('Actual observation probabililities\n', hmm.B)
print ('Estimated observation probabililities\n', hmmguess.B)

print("OK")
plt.subplot(2,1,2)
plt.cla()
plt.plot(np.vstack((s*0.9+0.05,hmmguess.gamma[1,:])).T,'-o',alpha=0.7)
plt.legend(('True State','Guessed Probability of State=1'))
plt.ylim(-0.1,1.1)
plt.xlabel('Time')
plt.draw()