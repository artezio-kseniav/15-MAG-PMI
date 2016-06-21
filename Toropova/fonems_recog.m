Input=wavread('fonems\3\01.wav');
std_i=[];
for j=1:3
X=wavread(strcat('fonems\',int2str(j),'\02.wav'));
AR=arburg(X,20)
Y=filter(AR,1,Input)
std_i(j)=std(Y)
end
[a,b]=min(std_i);
b