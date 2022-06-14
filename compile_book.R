
### Render book files:
system2("quarto", args = c("render", "--to html"))

### Clean Spark Warnings in outputs
source("clean_outputs.R", encoding = "UTF-8")