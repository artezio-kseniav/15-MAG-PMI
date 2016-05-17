require(WikipediR)
require(dplyr)
require(stringr)

dataset <- replicate(50, expr = random_page(language = "en", project = "wikinews", as_wikitext = TRUE, namespaces = "0") %$%
                    parse %>% as_data_frame, simplify = FALSE) %>%
    rbind_all %>%
  mutate(wikitext = unlist(wikitext, use.names = FALSE) %>% str_replace_all("[^[:print:]]"," "),
         categories = str_match_all(wikitext, "Category:([^\\]]*)") %>%
           sapply(. %>% {paste(.[,2], collapse = ", ")}))



dataset$wikitext %<>% str_replace_all("==[:space:]*(Related News|Sources)[:print:]*", " ") %>%
  str_replace_all("[:space:]+", " ")
