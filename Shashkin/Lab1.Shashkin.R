sapply(c("magrittr","quanteda","Rtsne","slam","dplyr","ggplot2","stringr","fastcluster"),
       require, character.only = TRUE)

# Load and rename duplicate data

setwd("~/Documents/Karpov/")
download.file("http://qwone.com/~jason/20Newsgroups/20news-18828.tar.gz", destfile = "20news-18828.tar.gz")
untar("20news-18828.tar.gz")
setwd("20news-18828/")

list.files(full.names = TRUE, recursive = TRUE) %>% {
  file.rename(., paste(., format(runif(length(.)), digits = 8, nsmall = 8, decimal.mark = ""), ".txt", sep = ""))
}

data <- textfile(list.files(full.names = TRUE, recursive = TRUE, pattern = "*.txt")) %>% corpus
metadoc(data,"class") <- list.files(recursive = TRUE, include.dirs = TRUE, pattern = "*.txt") %>% dirname

# TFIDF document term matrix > cosine distance matrix > hclust ward clusters & tsne embeding

sparse_cosine <- function(x){
  sq_cs <- col_sums(x^2)
  1 - crossprod_simple_triplet_matrix(x)/(sqrt(sq_cs %*% t(sq_cs)))
}

doc_dist <- dfm(data, stem = TRUE, toLower = TRUE, removeNumbers = TRUE, removePunct = TRUE, language = "english") %>%
  trim(minDoc = 2) %>%
  weight("tfidf") %>%
  convert("tm") %>%
  t %>% sparse_cosine

clusters <- fastcluster::hclust(d = as.dist(doc_dist), method = "ward.D") %>% cutree(k = 16)

embeding <- Rtsne(doc_dist, check_duplicates = FALSE, verbose = TRUE, is_distance = TRUE, max_iter = 4000)

# Visualize

plot_data <- metadoc(data, "class") %>%
  transmute(x       = embeding$Y[,1],
            y       = embeding$Y[,2],
            class   = factor(`_class`),
            cluster = factor(clusters)) %>%
  filter(!grepl(pattern = "misc", x = class))

plot_data %>%
  ggplot(aes(x = x, y = y)) +
  geom_density2d(aes(group = cluster), color = "grey50") +
  geom_jitter(aes(color = class), size = 0.7, width = 1, height = 1) +
  geom_text(data = plot_data %>% group_by(class) %>%
              summarise(x = median(x), y = median(y)),
            aes(x = x, y = y, label = class), size = 6) +
  scale_color_discrete(guide = FALSE) + theme_void()