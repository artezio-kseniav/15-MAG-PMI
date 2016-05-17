require(rvest)
require(magrittr)

link <- "http://izvestia.ru"

get_texts <- function(links){
  lapply(links, get_content)
}

get_content <- function(link){
  link %>% read_html() %>% 
    html_nodes("[itemprop=\"articleBody\"]") %>% 
    html_text
}

for (i in 1:1000){
  raw_html <- paste(link, "/archive/?type=0&p=", i, sep = "") %>% read_html 
  links <- raw_html %>% 
    html_nodes("h3 a") %>% 
    html_attr("href") %>% 
    paste(link, ., sep="")
  categories <- raw_html %>% 
    html_nodes(".info_block_rubric") %>% 
    html_text()
  titles <- raw_html %>% 
    html_nodes("h3 a") %>% 
    html_text()
  texts <- unlist(get_texts(links))
  appendix <- data.frame(links = links, categories=categories, titles=titles, texts=texts, stringsAsFactors = FALSE)
  write.table(appendix, "data/russian_corpus.csv", row.names=FALSE, append = TRUE, col.names = FALSE)
}

#df  <- read.table("/home/jule/karpov2.csv", 
#                  header = FALSE,
#                  col.names = c("links", "categories", "titles", "texts"), 
#                  stringsAsFactors = FALSE)
#df$categories  <- as.factor(df$categories)
