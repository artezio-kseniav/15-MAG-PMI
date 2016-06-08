require(readr)
require(stringr)
require(tm)

tbl <- read_tsv("/home/jule/labs/karpov/3grams-3.txt", col_names = F)[,-c(3,5)]
tbl$X1 <- tbl$X1/sum(tbl$X1)
tbl$three_grams <- paste(tbl$X2, tbl$X4, tbl$X6, sep = " ")
colnames(tbl)[1] <- "prob"
tbl <- subset(tbl, select = c(prob, three_grams))

saveRDS(tbl, "/home/jule/labs/karpov/3grams.RDS")

dfs <- lapply(15:17, function(x) {read.table(paste0("/home/jule/labs/karpov/data/", x,"_russian_corpus.csv"), 
                                             header = FALSE,
                                             col.names = c("links", "categories", "titles", "texts"), 
                                             stringsAsFactors = FALSE)})

df_politics <- dfs[[1]]
df_economics <- dfs[[2]]

get_3grams <- function(x, topic) {
  words <- gsub("[[:punct:]]", "", x, perl=TRUE) %>% 
    str_split(" ") %>% 
    unlist %>% 
    .[. != " "] %>%
    .[. != ""] 
  if(length(words) > 2){
    v1 <- words[1:(length(words)-2)]
    v2 <- words[2:(length(words)-1)]
    v3 <- words[3:(length(words))]
    write(length(words), paste0("/home/jule/labs/karpov/words", topic,".txt"), append = T)
    return(paste(v1, v2, v3))
  }
}

process_text <- function(x, topic) {
  clean_sentences <- str_split(x, "[.]") %>%
    unlist %>%
    str_trim(.) %>% 
    gsub("—", "", ., perl=TRUE) %>%
    gsub(pattern = "\\s+", repl = " ", str_trim(.)) %>%
    .[. != ""]
  lapply(clean_sentences, get_3grams, topic = topic) %>% unlist
}

three_grams_politics <- lapply(df_politics$texts, process_text, topic = "politics") %>% 
  unlist %>% 
  gsub(pattern = "\\s+", repl = " ", str_trim(.))

three_grams_economics <- lapply(df_economics$texts, process_text, topic = "economics") %>% 
  unlist %>% 
  gsub(pattern = "\\s+", repl = " ", str_trim(.))

perplexity <- function(x, topic) {
  model <- readRDS("/home/jule/labs/karpov/3grams.RDS")
  log_sum = lapply(x, function(x) log2(model$prob[model$three_grams == x]))  %>% 
    unlist  %>% 
    sum
  words_count = sum(read_tsv(paste0("/home/jule/labs/karpov/words", topic,".txt")))
  l <- log_sum/words_count
  2^(-l)
}

politics_perplexity <- perplexity(three_grams_politics, topic = "politics")
economics_perplexity <- perplexity(three_grams_politics, topic = "economics")

save("politics_perplexity", "economics_perplexity", file = "/home/jule/labs/karpov/perplexity.RData")

#additionally
#3 gram model for politics
politics_dictionary <- as.data.frame(table(three_grams_politics))
colnames(politics_dictionary) <- c("three_grams", "prob")
politics_dictionary$prob <- politics_dictionary$prob/sum(politics_dictionary$prob)
head(politics_dictionary)
