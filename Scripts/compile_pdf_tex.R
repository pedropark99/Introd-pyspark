library(tinytex)
TEX_FILE <- "Introduction-to-`pyspark`.tex"
PDF_FILE <- "Introduction-to-`pyspark`.pdf"

TEX_FILE <- "tex_adjusted.tex"
tinytex::xelatex(file = TEX_FILE, min_times = 2, max_times = 3, clean = TRUE)
# file.copy(
#   from = PDF_FILE,
#   to = paste0("docs/", PDF_FILE),
#   overwrite = TRUE
# )

# file.remove(PDF_FILE)