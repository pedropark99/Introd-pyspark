library(readr)
library(stringr)
library(purrr)
library(fs)

# "cell-output cell-output-stderr"

htmls <- fs::dir_ls(c("_book", "_book/Chapters"), glob = "*.html")

htmls <- map(htmls, read_file) |> 
  map(str_split, "\n") |> 
  map(unlist)

find_starts <- function(text){
  ids <- str_which(text, "<div class=\"cell-output cell-output-stderr\"")
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
  lines_to_keep <- seq_along(text)
  html_text <- text
  starts <- find_starts(text)
  ends <- find_ends(text, starts)
  diffs <- ends - starts
  lines_to_remove <- sequence.default(diffs + 1, from = starts)
  lines_to_keep <- !(lines_to_keep %in% lines_to_remove)
  return(html_text[lines_to_keep])
}

# remove_spark_warnings(htmls[[4]])

htmls <- htmls |> map(remove_spark_warnings)

for(html in names(htmls)){
  cat(str_c("Rewriting file: ", html, "\n"))
  write_file(str_c(htmls[[html]], collapse = "\n"), html)
}


