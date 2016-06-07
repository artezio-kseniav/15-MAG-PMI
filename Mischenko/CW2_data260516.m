%CW2 data 26.05.16
[yy, Fs, nbits] = wavread('zvuk_i.wav');
y = yy(:, 1);
y = y(4 * 10000 : 6 * 10000);
figure(), plot(y);
k = abs(fft(y));
x = linspace(0, 0.5, length(k) / 2);
figure(), plot(x, k(1:length(k)/2));
figure(), plot(x, 10*log10(k(1:length(k)/2)));
sd = 10*log10( pwelch(y, rectwin(480), 0) );
figure(), plot(linspace(0, 0.5, length(sd)), sd);