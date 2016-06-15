sapply(c("magrittr","quanteda","slam","dplyr","DT"), require, character.only = TRUE)

setwd("~/15-MAG-PMI/Shashkin/")

corpus <- readRDS("20newsgroups.RDS") +
  corpus("Computer science is the scientific and practical approach to computation and its applications. It is the systematic study of the feasibility, structure, expression, and mechanization of the methodical procedures (or algorithms) that underlie the acquisition, representation, processing, storage, communication of, and access to information. An alternate, more succinct definition of computer science is the study of automating algorithmic processes that scale. A computer scientist specializes in the theory of computation and the design of computational systems.[1]
         Its fields can be divided into a variety of theoretical and practical disciplines. Some fields, such as computational complexity theory (which explores the fundamental properties of computational and intractable problems), are highly abstract, while fields such as computer graphics emphasize real-world visual applications. Still other fields focus on challenges in implementing computation. For example, programming language theory considers various approaches to the description of computation, while the study of computer programming itself investigates various aspects of the use of programming language and complex systems. Human–computer interaction considers the challenges in making computers and computations useful, usable, and universally accessible to humans.")

dtm <- dfm(corpus, stem = TRUE, toLower = TRUE, removeNumbers = TRUE, removePunct = TRUE, language = "english") %>%
  trim(minDoc = 2)


# TFIDF

sparse_cosine <- function(x) {
  sq_cs <- col_sums(x ^ 2)
  crossprod_simple_triplet_matrix(x)/(sqrt(sq_cs %*% t(sq_cs)))
}

cos_sim <- dtm %>% weight("tfidf") %>% convert("tm") %>% t %>% sparse_cosine

# BM25

bm25 <- function(dtm, query, k = 1.6, b = 0.75) {
  f <- dtm[,which(as.vector(dtm[query,]) > 0)]
  n <- row_sums(dtm) %>% {k * (1 - b + b * . / mean(.))} %>% as.vector
  idf <- (col_sums(f > 0) + 0.5) %>% {log((dtm$nrow - .)/.)}

  (f * (k + 1) /
    (colapply_simple_triplet_matrix(f, FUN = `+`, n) %>% rbind_list %>% as.simple_triplet_matrix)
  ) %>% rowapply_simple_triplet_matrix(FUN = `*`, idf) %>% sapply(sum, USE.NAMES = FALSE)
}

bm_sim <- bm25(dtm %>% tf %>% convert("tm"), ndoc(corpus))

data_frame(tfidf = corpus$documents$texts[order(cos_sim[ndoc(corpus),], decreasing = TRUE)[1:10]],
           bm25 = corpus$documents$texts[order(bm_sim, decreasing = TRUE)[1:10]]) %>%
  datatable(caption = corpus$documents$texts[ndoc(corpus)]) %>%
  saveWidget('docsim_search_results.html')