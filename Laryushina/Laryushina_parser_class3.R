require(rvest)
require(magrittr)
require(doParallel)

cl <- makeCluster(detectCores() - 1)
registerDoParallel(cl)

link <- "http://izvestia.ru"

get_texts <- function(links){
  lapply(links, get_content)
}

get_content <- function(link){
  link %>% read_html() %>% 
    html_nodes("[itemprop=\"articleBody\"]") %>% 
    html_text %>% 
    gsub('[\"]',' ',.) %>% 
    gsub('[\t]',' ',.) %>% 
    gsub('[\n]',' ',.)
}

collect_corpus <- function(x){
  for (i in 1:150){
    raw_html <- paste(link, "/archive/", x, "?type=1&p=", i, sep = "") %>% read_html 
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
    write.table(appendix, paste0("labs/karpov/data/", x,"_russian_corpus.csv"), row.names=FALSE, append = TRUE, col.names = FALSE)
  }
}

foreach(i=15:17, .packages=c('magrittr', 'rvest')) %dopar% collect_corpus(i) %>% rm
