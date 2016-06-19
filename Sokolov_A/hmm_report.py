{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import sys\n",
    "from copy import copy\n",
    "import matplotlib.pyplot as plt"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "class HMM:\n",
    "    def __init__(self):\n",
    "        pass\n",
    "\n",
    "    def simulate(self,nSteps):\n",
    "\n",
    "        def drawFrom(probs):\n",
    "            return np.where(np.random.multinomial(1,probs) == 1)[0][0]\n",
    "\n",
    "        observations = np.zeros(nSteps)\n",
    "        states = np.zeros(nSteps)\n",
    "        states[0] = drawFrom(self.pi)\n",
    "        observations[0] = drawFrom(self.B[states[0],:])\n",
    "        for t in range(1,nSteps):\n",
    "            states[t] = drawFrom(self.A[states[t-1],:])\n",
    "            observations[t] = drawFrom(self.B[states[t],:])\n",
    "        return observations,states\n",
    "\n",
    "\n",
    "    def train(self,observations,criterion,graphics=False):\n",
    "        if graphics:\n",
    "            plt.ion()\n",
    "\n",
    "        nStates = self.A.shape[0]\n",
    "        nSamples = len(observations)\n",
    "\n",
    "        A = self.A\n",
    "        B = self.B\n",
    "        pi = copy(self.pi)\n",
    "\n",
    "        done = False\n",
    "        while not done:\n",
    "\n",
    "            # alpha_t(i) = P(O_1 O_2 ... O_t, q_t = S_i | hmm)\n",
    "            # Initialize alpha\n",
    "            alpha = np.zeros((nStates,nSamples))\n",
    "            c = np.zeros(nSamples) #scale factors\n",
    "            alpha[:,0] = pi.T * self.B[:,observations[0]]\n",
    "            c[0] = 1.0/np.sum(alpha[:,0])\n",
    "            alpha[:,0] = c[0] * alpha[:,0]\n",
    "            # Update alpha for each observation step\n",
    "            for t in range(1,nSamples):\n",
    "                alpha[:,t] = np.dot(alpha[:,t-1].T, self.A).T * self.B[:,observations[t]]\n",
    "                c[t] = 1.0/np.sum(alpha[:,t])\n",
    "                alpha[:,t] = c[t] * alpha[:,t]\n",
    "\n",
    "            # beta_t(i) = P(O_t+1 O_t+2 ... O_T | q_t = S_i , hmm)\n",
    "            # Initialize beta\n",
    "            beta = np.zeros((nStates,nSamples))\n",
    "            beta[:,nSamples-1] = 1\n",
    "            beta[:,nSamples-1] = c[nSamples-1] * beta[:,nSamples-1]\n",
    "            # Update beta backwards from end of sequence\n",
    "            for t in range(len(observations)-1,0,-1):\n",
    "                beta[:,t-1] = np.dot(self.A, (self.B[:,observations[t]] * beta[:,t]))\n",
    "                beta[:,t-1] = c[t-1] * beta[:,t-1]\n",
    "\n",
    "            xi = np.zeros((nStates,nStates,nSamples-1));\n",
    "            for t in range(nSamples-1):\n",
    "                denom = np.dot(np.dot(alpha[:,t].T, self.A) * self.B[:,observations[t+1]].T,\n",
    "                               beta[:,t+1])\n",
    "                for i in range(nStates):\n",
    "                    numer = alpha[i,t] * self.A[i,:] * self.B[:,observations[t+1]].T * \\\n",
    "                            beta[:,t+1].T\n",
    "                    xi[i,:,t] = numer / denom\n",
    "\n",
    "            # gamma_t(i) = P(q_t = S_i | O, hmm)\n",
    "            gamma = np.squeeze(np.sum(xi,axis=1))\n",
    "            # Need final gamma element for new B\n",
    "            prod =  (alpha[:,nSamples-1] * beta[:,nSamples-1]).reshape((-1,1))\n",
    "            gamma = np.hstack((gamma,  prod / np.sum(prod))) #append one more to gamma!!!\n",
    "\n",
    "            newpi = gamma[:,0]\n",
    "            newA = np.sum(xi,2) / np.sum(gamma[:,:-1],axis=1).reshape((-1,1))\n",
    "            newB = copy(B)\n",
    "\n",
    "            if graphics:\n",
    "                plt.subplot(2,1,1)\n",
    "                plt.cla()\n",
    "                #plt.plot(gamma.T)\n",
    "                plt.plot(gamma[1])\n",
    "                plt.ylim(-0.1,1.1)\n",
    "                plt.legend(('Probability State=1'))\n",
    "                plt.xlabel('Time')\n",
    "                plt.draw()\n",
    "\n",
    "            numLevels = self.B.shape[1]\n",
    "            sumgamma = np.sum(gamma,axis=1)\n",
    "            for lev in range(numLevels):\n",
    "                mask = observations == lev\n",
    "                newB[:,lev] = np.sum(gamma[:,mask],axis=1) / sumgamma\n",
    "\n",
    "            if np.max(abs(pi - newpi)) < criterion and \\\n",
    "                   np.max(abs(A - newA)) < criterion and \\\n",
    "                   np.max(abs(B - newB)) < criterion:\n",
    "                done = 1;\n",
    "\n",
    "            A[:],B[:],pi[:] = newA,newB,newpi\n",
    "\n",
    "        self.A[:] = newA\n",
    "        self.B[:] = newB\n",
    "        self.pi[:] = newpi\n",
    "        self.gamma = gamma\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {
    "collapsed": false,
    "scrolled": false
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "-----------------------------\n",
      "[ 0.  1.  2. ...,  2.  2.  2.]"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/home/artsokol/anaconda/lib/python2.7/site-packages/IPython/kernel/__main__.py:13: VisibleDeprecationWarning: using a non-integer number instead of an integer will result in an error in the future\n",
      "/home/artsokol/anaconda/lib/python2.7/site-packages/IPython/kernel/__main__.py:15: VisibleDeprecationWarning: using a non-integer number instead of an integer will result in an error in the future\n",
      "/home/artsokol/anaconda/lib/python2.7/site-packages/IPython/kernel/__main__.py:16: VisibleDeprecationWarning: using a non-integer number instead of an integer will result in an error in the future\n",
      "/home/artsokol/anaconda/lib/python2.7/site-packages/IPython/kernel/__main__.py:38: VisibleDeprecationWarning: using a non-integer number instead of an integer will result in an error in the future\n",
      "/home/artsokol/anaconda/lib/python2.7/site-packages/IPython/kernel/__main__.py:43: VisibleDeprecationWarning: using a non-integer number instead of an integer will result in an error in the future\n",
      "/home/artsokol/anaconda/lib/python2.7/site-packages/IPython/kernel/__main__.py:54: VisibleDeprecationWarning: using a non-integer number instead of an integer will result in an error in the future\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "[ 0.  0.  1. ...,  1.  1.  1.]\n",
      "('Actual probabilities\\n', array([ 0.5,  0.5]))\n",
      "('Estimated initial probabilities\\n', array([ 1.,  0.]))\n",
      "('Actual state transition probabililities\\n', array([[ 0.85,  0.15],\n",
      "       [ 0.12,  0.88]]))\n",
      "('Estimated state transition probabililities\\n', array([[ 0.84 ,  0.16 ],\n",
      "       [ 0.118,  0.882]]))\n",
      "('Actual observation probabililities\\n', array([[ 0.8,  0.1,  0.1],\n",
      "       [ 0. ,  0. ,  1. ]]))\n",
      "('Estimated observation probabililities\\n', array([[ 0.781,  0.106,  0.114],\n",
      "       [ 0.006,  0.   ,  0.994]]))\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/home/artsokol/anaconda/lib/python2.7/site-packages/IPython/kernel/__main__.py:59: VisibleDeprecationWarning: using a non-integer number instead of an integer will result in an error in the future\n",
      "/home/artsokol/anaconda/lib/python2.7/site-packages/IPython/kernel/__main__.py:62: VisibleDeprecationWarning: using a non-integer number instead of an integer will result in an error in the future\n"
     ]
    }
   ],
   "source": [
    "if __name__ == '__main__':\n",
    "    np.set_printoptions(precision=3,suppress=True)\n",
    "    # if True:\n",
    "    #'Two states, three possible observations in a state'\n",
    "    #\n",
    "    hmm = HMM()\n",
    "    hmm.pi = np.array([0.5, 0.5]) # всего 2 состояния\n",
    "    hmm.A = np.array([[0.85, 0.15], [0.12, 0.88]]) # матрица переходов\n",
    "    hmm.B = np.array([[0.8, 0.1, 0.1], [0.0, 0.0, 1]]) # 1 состояние (строка) порождает наблюдения для 1 строки\n",
    "    # # для второго состояния получим только 3 наблюдение\n",
    "    #\n",
    "    hmmguess = HMM()\n",
    "    hmmguess.pi = np.array([0.5, 0.5])\n",
    "    hmmguess.A = np.array([[0.5, 0.5],\n",
    "                          [0.5, 0.5]])\n",
    "    hmmguess.B = np.array([[0.3, 0.3, 0.4],\n",
    "                          [0.2, 0.5, 0.3]])\n",
    "    # else:\n",
    "    #three states\n",
    "    #print(\"Error....this example with three states is not working correctly.\")\n",
    "\n",
    "    o,s = hmm.simulate(5000)\n",
    "    print(o)\n",
    "    print(s)\n",
    "\n",
    "    # sys.exit()\n",
    "    hmmguess.train(o,0.0001,graphics=True)\n",
    "\n",
    "    print('Actual probabilities\\n',hmm.pi)\n",
    "    print('Estimated initial probabilities\\n',hmmguess.pi)\n",
    "\n",
    "    print('Actual state transition probabililities\\n',hmm.A)\n",
    "    print('Estimated state transition probabililities\\n',hmmguess.A)\n",
    "\n",
    "    print('Actual observation probabililities\\n',hmm.B)\n",
    "    print('Estimated observation probabililities\\n',hmmguess.B)\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "hmm = HMM()\n",
    "hmm.pi = np.array([0.1, 0.4, 0.5])\n",
    "hmm.A = np.array([[0.7, 0.2, 0.1],\n",
    "                  [0.1, 0.6, 0.3],\n",
    "                  [0.4, 0.2, 0.4]])\n",
    "hmm.B = np.array([[0.5, 0.3, 0.2],\n",
    "                  [0.1, 0.6, 0.3],\n",
    "                  [0.0, 0.3, 0.7]])\n",
    "    print(\"-----------------------------\")\n",
    "hmmguess = HMM()\n",
    "hmmguess.pi = np.array([0.333, 0.333, 0.333])\n",
    "hmmguess.A = np.array([[0.3333, 0.3333, 0.3333],\n",
    "                       [0.3333, 0.3333, 0.3333],\n",
    "                       [0.3333, 0.3333, 0.3333]])\n",
    "hmmguess.B = np.array([[0.3, 0.3, 0.4],\n",
    "                       [0.2, 0.5, 0.3],\n",
    "                       [0.3, 0.3, 0.4]])\n",
    "\n",
    "o,s = hmm.simulate(5000)\n",
    "print(o)\n",
    "print(s)\n",
    "\n",
    "# sys.exit()\n",
    "hmmguess.train(o,0.0001,graphics=True)\n",
    "\n",
    "print('Actual probabilities\\n',hmm.pi)\n",
    "print('Estimated initial probabilities\\n',hmmguess.pi)\n",
    "\n",
    "print('Actual state transition probabililities\\n',hmm.A)\n",
    "print('Estimated state transition probabililities\\n',hmmguess.A)\n",
    "\n",
    "print('Actual observation probabililities\\n',hmm.B)\n",
    "print('Estimated observation probabililities\\n',hmmguess.B)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.text.Text at 0x7f3e942b6290>"
      ]
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "plt.subplot(2,1,2)\n",
    "plt.cla()\n",
    "plt.plot(np.vstack((s*0.9+0.05,hmmguess.gamma[1,:])).T,'-o',alpha=0.7)\n",
    "plt.legend(('True State','Guessed Probability of State=1'))\n",
    "plt.ylim(-0.1,1.1)\n",
    "plt.xlabel('Time')\n",
    "#plt.draw()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 2",
   "language": "python",
   "name": "python2"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 2
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython2",
   "version": "2.7.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 0
}
