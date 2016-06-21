require(phonTools)

s<-loadsound("a.wav")
findformants(s)

require(tuneR)
require(seewave)
require(signal)

f <- readWave("a.wav")
sprintf("length = %d ms",length(f@left)/f@samp.rate * 1000)
Fs<-s[[2]]
part_num <-1
X <- f@left
X_cut <- X[part_num*Fs/100:(part_num+1)*Fs/100];
X_cut_ham <- hamming(length(X_cut))*X_cut

y <- abs(fft(X, 1024));
y_cut <- abs(fft(X_cut, 1024));
y_cut_ham <- abs(fft(X_cut_ham, 1024));

plot(y)

n <- length(f@left)
p <- fft(f@left)
nUniquePts <- ceiling((n+1)/2)
p <- p[1:nUniquePts]
p <- abs(p)
p <- p / n 
p <- p^2

if (n %% 2 > 0){
  p[2:length(p)] <- p[2:length(p)]*2
} else {
  p[2: (length(p) -1)] <- p[2: (length(p) -1)]*2
}

freqArray <- (0:(nUniquePts-1)) * (f@samp.rate / n)

plot(freqArray/1000, 10*log10(p), type='l', col='black', xlab='Frequency (kHz)', ylab='Power (dB)')