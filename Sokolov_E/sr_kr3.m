[a, Fs1, nbits1, opts1] = wavread('C:/linguistics/�.wav');
[o, Fs2, nbits2, opts2] = wavread('C:/linguistics/�.wav');
[u, Fs3, nbits3, opts3] = wavread('C:/linguistics/�.wav');

std_all=[];
input = u;
ara = arburg(a, 20);
fa = filter(ara,1,input); 
std_all(1) = std(fa);
plot(fa)
% 1 ar - ����������� 
% ar 1 - ��������� ������

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
