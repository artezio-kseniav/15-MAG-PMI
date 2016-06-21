require(wordVectors)
require(magrittr)
require(parallel)
require(readr)
require(R2HTML)

setwd(paste0(getwd(), "/labs/"))

threads = detectCores() - 1 

data_path <- "data/20news-18828/alt.atheism/"

combined <- prep_word2vec(data_path, dest = "w2w.rdata", lowercase = T)

model <- train_word2vec("output/w2w.rdata", threads = threads, 
                        vectors = 300, window = 10, min_count = 10, cbow = 1)

vectors <- read.vectors("output/w2w.bin")

nearest_to(vectors, vectors[["koresh"]])

nearest_to(vectors, vectors[["god"]] - vectors[["man"]] + vectors[["woman"]])

nearest_to(vectors, vectors[["god"]] - vectors[["he"]] + vectors[["she"]])

god_names = nearest_to(vectors, vectors[[c("god","gods","lord","master")]], 10)
plot(filter_to_rownames(vectors, names(god_names)))

evilless = vectors[["god"]] %>%
  reject(vectors[["satan"]]) %>% 
  reject(vectors[["evil"]]) %>% 
  reject(vectors[["she"]])
vectors %>% nearest_to(evilless)