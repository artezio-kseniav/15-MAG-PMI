require(WikipediR)
require(magrittr)

corpus <- replicate(100, simplify = FALSE,
                    expr = WikipediR::query("en.wikinews.org/w/api.php?format=json&action=query&list=random&rnlimit=500&rnnamespace=0", NULL)) %>%
  unlist %>% {.[names(.) == "query.random.id"]} %>% unique %>%
  paste("en.wikinews.org/w/api.php?format=json&action=parse&prop=wikitext|categories&pageid=",.,sep = "") %>%
  lapply(WikipediR::query, "pcontent")

require(dplyr)
require(purrr)
require(stringr)

corpus %<>%
  map(. %>% flatten %$%
        data_frame(id = pageid,
                   title = title,
                   text = wikitext$`*`,
                   categories = categories %>%
                     unlist %>% {.[names(.) == "*"]} %>% paste(collapse = "|"))) %>%
  rbind_all %>%
  mutate(text = text %>% str_replace_all("[^[:print:]]"," ") %>%
           str_replace_all("==([:space:]*)(Related news|Sources)([:space:]*)==([:print:]*)", " ") %>%
           str_replace_all("\\{{2}([A|a]rchive|Audio|date|[I|i]mage|[H|h]aveyour|HYS|[S|s]ource|[P|p]ublish)[^{}]*\\}{2}"," ") %>%
           str_replace_all("[:space:]+", " ") %>% trimws("both"))

# 2 hours ~= 20k documents ~= 20Mb
saveRDS(corpus, "wikinews.RDS")

corpus %<>%
  str_replace_all("\\[{2}(Category|File|Image|User|Portal):[^\\]{2}]*\\]{2}", " ") %>%
  str_replace_all("\\[{2}([^\\||\\]{2}|:]*)\\]{2}"," \\1 ") %>%
  str_replace_all("\\{{2}([^\\||\\}{2}|:]*)\\}{2}"," \\1 ") %>%
  str_replace_all("\\|([^\\||\\]{2}]+)\\]{2}", "\\]\\] \\1 ") %>%
  str_replace_all("\\[{2}[^\\]{2}]*\\]{2}", " ") %>%
  str_replace_all("\\{{2}[^\\}{2}]*\\}{2}", " ")


