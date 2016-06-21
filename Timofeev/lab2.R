require(tuneR)
require(seewave)
require(signal)

f <- readWave("a.wav")
plot(f@left, type="l")

f2 <- readWave("o.wav")
lines(f2@left, col="red")

f3 <- readWave("i.wav")
lines(f3@left, col="green")


coef <- ar.burg(f@left, order.max = 20)

filter <- Arma(a = coef$ar, rep(1,5))

x <- signal::filter(filt = filter, x = f@left)

plot(x, type = "l")
lines(f@left, col = "pink")
