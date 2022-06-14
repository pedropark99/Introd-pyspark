library(readr)
library(stringr)
library(purrr)

### Render book files specifically to PDF:
system2("quarto", args = c("render", "--to pdf"))

name_file <- "Introduction-to-`pyspark`.tex"
tex_file <- read_file(name_file)
tex_file <- tex_file |> 
  str_split("\n") |> 
  unlist()

find_verbatim_blocks <- function(tex){
  starts <- str_which(tex, "^\\\\begin\\{verbatim\\}")
  ends <- str_which(tex, "^\\\\end\\{verbatim\\}")
  
  # diffs <- ends - starts + 1
  # ranges <- sequence.default(from = starts, nvec = diffs)

  return(list(starts = starts, ends = ends))
}


detect_target_messages<- function(verbatim_start, verbatim_end, tex, pattern){
  range <- verbatim_start:verbatim_end
  contain_target_messages <- tex[range] |> 
    str_detect(pattern) |> 
    any()
  
  if (contain_target_messages) {
    tex[range] <- "\n"
  }
  
  return(tex)
}


warning_pattern <- "^[0-9]{2}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} WARN"
stage_pattern <- "^\\[Stage ([0-9]*):>"
log4j_pattern <- "^Using Spark's default log4j profile:"



verbatim <- find_verbatim_blocks(tex_file)
for (i in seq_along(verbatim$starts)) {
  tex_file <- detect_target_messages(verbatim$starts[i], verbatim$ends[i], tex_file, warning_pattern)
  tex_file <- detect_target_messages(verbatim$starts[i], verbatim$ends[i], tex_file, stage_pattern)
  tex_file <- detect_target_messages(verbatim$starts[i], verbatim$ends[i], tex_file, log4j_pattern)
}


write_file(str_c(tex_file, collapse = "\n"), name_file)



### Rename tex file to avoid conflicts
new_name <- str_replace_all(name_file, "`", "")
fs::file_move(name_file, new_name)

just_name <- str_sub(new_name, 1, str_length(new_name) - 4)
system(paste("xelatex", shQuote(just_name)))
system(paste("bibtex", shQuote(just_name)))
system(paste("xelatex", shQuote(just_name)))


### Delete unnecessary files produced by Latex
file_names <- c(new_name, name_file)
just_names <- str_sub(file_names, 1, str_length(file_names) - 4)
just_names <- rep(just_names, each = 3)
files_to_delete <- sprintf("%s%s", just_names, c(".aux", ".log", ".toc"))
fs::file_delete(files_to_delete)

