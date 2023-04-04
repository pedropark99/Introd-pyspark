

knitr::knit_engines$set(terminal = function(options) {
  code <- paste(options$code, collapse = "\n")
  code_to_run <- stringr::str_replace(
    code, "^Terminal\\$ ", ""
  )
  code <- stringr::str_replace(
    code, "^Terminal\\$ ",
    '\n<span class="im">Terminal$</span>\n'
  )
  out <- system(code_to_run)

  knitr::engine_output(options, code, out)
})