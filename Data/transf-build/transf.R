library(tidyverse)

institution_number <- '012'
branch_numbers <- sample(as.character(c(5214, 4095, 2620, 1311)), size = 1545, replace = TRUE)
account_numbers <- sample(as.character(12300:99000), size = 1545, replace = TRUE)

account_infos <- tibble(
  bankNumber = institution_number,
  branchNumber = branch_numbers,
  accountNumber = account_numbers
)
