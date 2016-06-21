% [X, Fs, nbits, opts] = wavread('D:/fffile.wav');
input = wavread('D:/praat/o_artem.wav');
%arinpunt = arburg(input, 20)
%finput = filter(arinput, 1, input)

[a, Fs1, nbits1, opts1] = wavread('D:/praat/a.wav');
[o, Fs2, nbits2, opts2] = wavread('D:/praat/o.wav');
[u, Fs3, nbits3, opts3] = wavread('D:/praat/u.wav');

std_all=[];
input = u;
% a sound
ara = arburg(a, 20);
% plot(a)
fa = filter(ara,1,input); 
std_all(1) = std(fa);
plot(fa)
% 1 ar - порождающий 
% ar 1 - обел€ющий фильтр

% o sound
aro = arburg(o, 20);
fo = filter(aro,1,input); 
std_all(2) = std(fo);

% u sound
aru = arburg(u, 20);
fu = filter(aru,1,input); 
std_all(3) = std(fu);

[a, i] = min(std_all);
i
