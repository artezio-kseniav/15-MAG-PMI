% [X, Fs, nbits, opts] = wavread('D:/fffile.wav');
[X, Fs, nbits, opts] = 	('D:/praat/iii_8000.wav');
part_num = 1
X_cut = X(part_num*Fs/100:(part_num+1)*Fs/100);
X_cut_ham = hamming(length(X_cut)).*X_cut
length(X)/Fs % ������ ������
% plot(X)
y = abs(fft(X, 1024));
y = abs(fft(X_cut, 1024));
y_cut_ham = abs(fft(X_cut_ham, 1024));
%  plot(abs(y)) % ������
I = (1:length(y)/2)/length(y);
% plot(I,y(1:length(y)/2)) % �� ������ [0;0.5]
half_y = y(1:length(y)/2);
log_y = 10*log10(half_y);
hold('on')
plot(I,log_y, 'color', 'r')

y = y_cut_ham
half_y = y(1:length(y)/2);
log_y = 10*log10(half_y);
plot(I,log_y, 'color', 'b')
hold('off')