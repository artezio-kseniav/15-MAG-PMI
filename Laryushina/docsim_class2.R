setwd(paste0(getwd(), "/karpov/cl/"))
data_path <- "data/20news-18828/"

require(magrittr)
require(quanteda)
require(readr)
require(qlcMatrix)
require(tm)

query <- "See the listing for African Americans for Humanism above."

files <- list.files(data_path, recursive = TRUE) %>% 
  paste0(getwd(), "/", data_path, .) 

corp <- lapply(files, read_file) %>% 
  unlist %>% 
  corpus %T>% 
  saveRDS(paste0(getwd(), "/data/", "20NewsCorpus.RDS"))

get_dfm <- function(corpus){
  df_m <- dfm(corpus, 
              stem = TRUE, toLower = TRUE, removeNumbers = TRUE, 
              removeTwitter = TRUE, removePunct = TRUE, language = "english") 
  
  df_m %<>% trim(., minCount = 2, minDoc = 2) %>% 
    selectFeatures(stopwords("english"), "remove", valuetype = "fixed")
  df_m
}

bm25_transform <- function (dtm, k = 2, b = 0.5) {
  doc_mean <- mean(rowapply_simple_triplet_matrix(dtm, sum))
  doc_length <- row_sums(dtm)
  x <- dtm*(k+1)/(dtm + as.simple_triplet_matrix(matrix(rep(k*(1-b+b*doc_length/doc_mean),ncol(dtm)),ncol=ncol(dtm))))
  result <- x/row_sums(x)
  result
}

get_cosine <- function(df_m){
  tfidf <- tfidf(df_m, normalize = TRUE)
  cosine <- cosSparse(tfidf %>% t)
  cosine
}

find_similar_cosine <- function(corpus, query){
  combined <- rbind(get_dfm(corpus), dfm(query, verbose = FALSE))
  matr <- get_cosine(combined)
  order(matr[ndoc(combined),], decreasing = T)[2:11]
}

ind <- find_similar_cosine(corp, query)
files[ind]
