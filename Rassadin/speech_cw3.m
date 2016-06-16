[yy1, Fs1, nbits1] = wavread('4/03.wav');
[yy2, Fs2, nbits2] = wavread('5/02.wav');
[yy3, Fs3, nbits3] = wavread('6/07.wav');
y1 = yy1(:, 1);
y2 = yy2(:, 1);
y3 = yy3(:, 1);
% figure(), plot(y1);
% figure(), plot(y2);
% figure(), plot(y3);
[a1, g1] = lpc(y1, 4);
[a2, g2] = lpc(y2, 4);
[a3, g3] = lpc(y3, 4);
Y1 = filter(1.0 / 10, a1, yy1);
Y2 = filter(1.0 / 7, a2, yy2);
Y3 = filter(1.0 / 18, a3, yy3);
% Y1 = filter(a1, 1 / 3, yy1);
% Y2 = filter(a2, 1, yy2);
% Y3 = filter(a3, 1, yy3);
% figure(), plot(Y1);
% figure(), plot(Y2);
% figure(), plot(Y3);
std1 = std(Y1);
std2 = std(Y2);
std3 = std(Y3);

err11 = abs(std(y1) - std1);
err12 = abs(std(y1) - std2);
err13 = abs(std(y1) - std3);
err21 = abs(std(y2) - std1);
err22 = abs(std(y2) - std2);
err23 = abs(std(y2) - std3);
err31 = abs(std(y3) - std1);
err32 = abs(std(y3) - std2);
err33 = abs(std(y3) - std3);