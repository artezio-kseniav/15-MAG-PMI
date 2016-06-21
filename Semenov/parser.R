require(rvest)
require(magrittr)
require(stringi)

link <- "http://www.theatlantic.com"

get_text <- function(link){
  link %>% read_html() %>% 
    html_nodes("#article-section-1")  %>% 
    html_text %>% 
    gsub('[\"]',' ',.)
}

get_title <- function(link){
  link %>% read_html() %>% 
    html_nodes("h1.hed")  %>% 
    html_text
}

get_category <- function(link){
  link %>% read_html() %>% 
    html_nodes(".rubric")  %>% 
    html_text  %>% 
    stri_replace_all_charclass("\\p{WHITE_SPACE}", "")
}

for (i in 1:1000){
  raw_html <- paste(link, "/news/?page=", i, sep = "") %>% read_html 
  links <- raw_html %>% 
    html_nodes(".blog-article a") %>% 
    html_attr("href") %>% 
    paste(link, ., sep="")
  links <- links[!grepl("*author*", links) & !grepl("*disqus_thread*", links)]
  categories <- unlist(lapply(links, get_category))
  titles <- unlist(lapply(links, get_title))
  texts <- unlist(lapply(links, get_text))
  appendix <- data.frame(links = links, categories=categories, titles=titles, texts=texts, stringsAsFactors = FALSE)
  write.table(appendix, "data/english_corpus.csv", row.names=FALSE, append = TRUE, col.names = FALSE)
}