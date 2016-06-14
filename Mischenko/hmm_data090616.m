%trans = ['н1 о2 ль3','о2 д4 и5 н1', 'д4 в6 а7', 'т8 р9 и5', 'ч10 и5 т8 ы11 р9 и5','пь12 а7 ть13', 'ш14 э15 с16 ть13', 'сь17 э15 мь18' 'в6 о2 сь17 и5 мь18' 'д4 евьать']
trans1 = [[1,2,3], [2, 4, 5, 1], [4, 6, 7], [8, 9 5], 'ч е т ы ре','пь а ть']

trans = [0.95,0.05; 0.10,0.90];
emis = [1/6 1/6 1/6 1/6 1/6 1/6;
   1/10 1/10 1/10 1/10 1/10 1/2];

[seq,states] = hmmgenerate(100,trans,emis);
[estimateTR,estimateE] = hmmestimate(seq,states);

estimatedStates = hmmviterbi(seq,trans,emis);

pStates = hmmdecode(seq,trans,emis);

seq1 = hmmgenerate(100,trans,emis);
seq2 = hmmgenerate(200,trans,emis);
seqs = {seq1,seq2};
[estTR,estE] = hmmtrain(seqs,trans,emis);

sum(states==estimatedStates)/1000

PSTATES = hmmdecode(seq,trans,emis)