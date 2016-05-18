require(WikipediR)
require(dplyr)
require(stringr)
require(magrittr)
require(purrr)

system.time(
  dataset <- replicate(5000, expr = try(random_page(domain = "en.wikinews.org",
                                                   as_wikitext = TRUE,
                                                   namespaces = "0")),
                     simplify = FALSE)
)



%>%
    rbind_all %>%
  mutate(wikitext = unlist(wikitext, use.names = FALSE) %>% str_replace_all("[^[:print:]]"," "),
         categories = str_match_all(wikitext, "Category:([^\\]]*)") %>%
           sapply(. %>% {paste(.[,2], collapse = ", ")}))



dataset$wikitext %<>% str_replace_all("==[:space:]*(Related News|Sources)[:print:]*", " ") %>%
  str_replace_all("[:space:]+", " ")
