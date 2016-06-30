input = wavread('a_praat.wav');

[a, Fs1, nbits1, opts1] = wavread('D:/praat/a.wav');
[o, Fs2, nbits2, opts2] = wavread('D:/praat/o.wav');
[u, Fs3, nbits3, opts3] = wavread('D:/praat/u.wav');

std_all=[];

ara = arburg(a, 20);

fa = filter(ara,1,input); 
std_all(1) = std(fa);
plot(fa)

aro = arburg(o, 20);
fo = filter(aro,1,input); 
std_all(2) = std(fo);

aru = arburg(u, 20);
fu = filter(aru,1,input); 
std_all(3) = std(fu);

[a, i] = min(std_all);
i
