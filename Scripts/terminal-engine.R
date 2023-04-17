

knitr::knit_engines$set(terminal = function(options) {
  code <- paste(options$code, collapse = "\n")
  code_to_run <- stringr::str_replace_all(
    code, "Terminal\\$ ", ""
  )
  code_to_run <- paste0("bash -c ", shQuote(code_to_run), collapse = "")
  out <- system(code_to_run, intern = TRUE)
  out <- out[!is_log_info(out)]

#   code <- stringr::str_replace_all(
#     code, "Terminal\\$ ",
#     '\n<span class="im">Terminal$</span>\n'
#   )
  
  knitr::engine_output(options, code, out)
})


is_log_info <- function(output) {
    log_regex <- "[0-9]{2}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} WARN|\\[Stage "
    stringr::str_detect(output, log_regex)
}


