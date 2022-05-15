library(readr)
library(stringr)
library(purrr)
library(fs)

htmls <- fs::dir_ls("_book", glob = "*.html")

htmls <- map(htmls, read_file) |> 
  map(str_split, "\n") |> 
  map(unlist)

find_starts <- function(text){
  ids <- str_which(text, "<div class=\"cell-output cell-output-stderr\">")
  return(ids)
}

find_ends <- function(text, starts){
  div_ids <- str_which(text, "</div>")
  ends <- vector("integer", length = length(starts))
  for(i in seq_along(starts)){
    start <- starts[i]
    candidates <- div_ids[div_ids > start]
    candidates <- sort(candidates)
    ends[i] <- candidates[1]
  }
  return(ends)
}



remove_spark_warnings <- function(text){
  html_text <- text
  starts <- find_starts(text)
  ends <- find_ends(text, starts)
  pattern <- "Using Spark's default log4j profile|[0-9]{2}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} WARN"
  for(i in seq_along(starts)){
    start <- starts[i]
    end <- ends[i]
    remove <- any(str_detect(html_text[start:end], pattern))
    if(remove) html_text[start:end] <- "\n"
  }
  return(html_text)
}

# remove_spark_warnings(htmls[[4]])

htmls <- htmls |> map(remove_spark_warnings)

for(html in names(htmls)){
  cat(str_c("Rewriting file: ", html, "\n"))
  write_file(str_c(htmls[[html]], collapse = "\n"), html)
}


