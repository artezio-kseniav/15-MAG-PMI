require(quanteda)
require(readr)
require(dplyr)

corpus <- readRDS("ruwikinews.RDS")

data <- corpus$text %>% dfm(toLower = TRUE,
                            removeNumbers = TRUE,
                            removePunct = TRUE,
                            stem = FALSE, ngrams = 3) %>%
  colSums %>% {data_frame(token = names(.), n = .)}

model <- read_tsv("3grams-3.txt", col_names = FALSE) %>%
  transmute(token = paste(X2,X4,X6, sep = "_"), freq = X1/sum(X1))

model %>% inner_join(data) %$% 2^(-sum(n*log2(freq))/nrow(model))

# 1.742602