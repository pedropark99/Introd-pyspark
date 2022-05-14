knitr::knit_engines$set(spark = function(options){
  code <- paste(options$code, collapse = "\n")
  if(Sys.info()["sysname"] == "Linux"){
    cmd <- "python3"
  } else {
    cmd <- "python"
  }
  
  result <- system2(cmd, args = c("-c", shQuote(code)))
  return(result)
})


