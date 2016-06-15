require(wordVectors)
require(magrittr)
require(quanteda)

corpus <- readRDS("15-MAG-PMI/Shashkin/20newsgroups.RDS")

vocab <- corpus %>% dfm(toLower = TRUE, removeNumbers = TRUE, removePunct = TRUE,
                        removeURL = TRUE, removeSymbols = TRUE, stem = TRUE,
                        language = "english") %>%
  trim(minCount = 10, minDoc = 10) %>% {.@Dimnames$features}

corpus %>% toLower %>% tokenize(what = "sentence") %>% unlist %>%
  tokenize("word", removeNumbers = TRUE, removePunct = TRUE,
           removeURL = TRUE, removeSymbols = TRUE) %>%
  wordstem("english") %>%
  selectFeatures(vocab, "keep") %>%
  sapply(paste0, collapse = " ") %>%
  cat(file = "w2v_data", sep = " ")

train_word2vec(train_file = "w2v_data", output_file = "w2v_model",
               vectors = 100, threads = 4, window = 6, iter = 10)

w2v <- read.binary.vectors("w2v_model")

nearest_to(w2v, w2v[["car"]])