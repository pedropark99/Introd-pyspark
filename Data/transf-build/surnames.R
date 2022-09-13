library(rvest)
a <- rvest::read_html("Data/transf-build/surnames.html")

a %>% 
  html_element("table") %>% 
  html_table()

b <- a |> 
  rvest::html_elements("td") |> 
  rvest::html_text() |> 
  as.character()


id <- str_which(b, "<td><p><a")
surnames <- str_c(b[id], collapse = '\n') |> rvest::read_html()

surnames <- surnames |> 
  rvest::html_elements('a') |> 
  rvest::html_text()


firstnames <- readxl::read_excel("Data/transf-build/names.xlsx")
firstnames$first <- str_to_title(firstnames$first)

