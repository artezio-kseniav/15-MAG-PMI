k=0;
cep=zeros(1000,21);
for j=0:1:9
	for i=0:1:99
		if i>9 strnum = int2str(i);
		else strnum = strcat('0',int2str(i));
		end
		[signal,Fs] = wavread(strcat('sounds\numeral\',int2str(j),'\',strnum,'.wav'));
		for st=Fs/100:Fs/100:length(signal)
			k=k+1;
			frame=signal(st-Fs/100+1:st);
			AR = arburg(frame,20)';
			cep(k,:) = lpc_to_cep(AR'(2:length(AR)));
		end
	end
end
[IDX, С] = kmeans (cep, 256)

%plot(cep)