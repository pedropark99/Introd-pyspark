library(tidyverse)

names <- c(
  "Anne Frank", "Michael Scott", "Pam Beesly", "Jim Halpert",
  "Dwight Schrute", "Angela Martin", "Kelly Kapoor", "Ryan Howard",
  "Troy Bolton", "Gabriella Montez", "Sharpay Evans",
  "Gina Weasley", "Harry Potter", "Hermione Granger",
  "Jake Peralta", "Rosa Diaz", "Amy Santiago", "Gina Linetti", "Ray Holt",
  "Charles Boyle", "Edward Elric", "Alphonse Elric", "Roy Mustang",
  "Winry Rockbell", "Maes Hughes", "Ling Yao"
)

cities <- c(
  "Amsterdam", rep("Scranton", times = 7),
  rep("Salt Lake", times = 3), rep("London", times = 3),
  rep("New York", times = 6), rep("Central City", times = 6)
)

countries <- c(
  "Netherlands", rep("United States", times = 10),
  rep("United Kingdom", times = 3), rep("United States", times = 6),
  rep("Amestris", times = 6)
)

streets <- c(
  "Boomstraat", "Foster St", "Meade Ave", "Gunster Ave",
  "Hawk Pi", "Ward Pi", "Bartel St", "Penn Ave",
  "300 N", "Euclid Ave", "Patricia Way",
  "Seymour Rd", "Duckett Rd", "Cavendish Rd",
  "Washington Ave", "Prescott St", "Spruce St",
  "Lefferts Rd", "Claydon Rd", "Kenwood Rd",
  "Laurel", "Mullberry", "Avalon", "Central Ring",
  "Central Ring", "Royal Garden"
)

set.seed(450)
numbers <- sample(12:450, size = length(names), replace = TRUE)
branchs <- c(3321L, 4425L, 1979L, 8521L)
branchs <- sample(branchs, size = length(names), replace = TRUE)
account_numbers <- sample(24561:86421, size = length(names))
account_numbers <- str_c(account_numbers, "-", sample(0:9,size = length(names), replace = TRUE))


accounts <- tibble(
  clientNumber = sample(1114:6532, size = length(names)),
  clientName = names,
  branchNumber = branchs,
  accountNumber = account_numbers,
  addressCountry = countries,
  addressCity = cities,
  adressStreet = streets,
  adressNumber = numbers
)


write_csv(accounts, "Data/accounts.csv")






set.seed(555)
dates <- seq.Date(as.Date("2022-01-01"), as.Date("2022-12-31"), by = 1)
dates <- sample(dates, size = 2421, replace = TRUE)
set.seed(129)
hours <- sample(0:23, size = 2421, replace = TRUE)
set.seed(321)
minutes <- sample(0:59, size = 2421, replace = TRUE)
set.seed(1240)
seconds <- sample(0:59, size = 2421, replace = TRUE)

format_time <- function(x){
  need_ajustment <- x < 10
  as_text <- as.character(x)
  as_text[need_ajustment] <- str_c("0", as_text[need_ajustment])
  as_text
}

hours <- hours %>% format_time()
minutes <- minutes %>% format_time()
seconds <- seconds %>% format_time()

times <- sprintf("%s:%s:%s", hours, minutes, seconds)
datetimes <- sprintf("%s %s", dates, times)


transfer_values <- rnorm(n = 2421, mean = 6295, sd = 2500)
transfer_values[transfer_values < 0] <- transfer_values[transfer_values < 0] * -1
transfer_values[transfer_values < 50] <- transfer_values[transfer_values < 50] * 10 
transfer_values <- as.integer(transfer_values)
set.seed(890)
offsets <- round(rnorm(2421), 2)
random_indexes <- sample(seq_along(offsets), size = length(offsets) / 2)
offsets[random_indexes] <- 0
transfer_values <- transfer_values + offsets


client_numbers <- sample(accounts$clientNumber, size = 2421, replace = TRUE)

transf <- tibble(
  dateTransfer = lubridate::as_date(dates),
  datetimeTransfer = lubridate::as_datetime(datetimes),
  clientNumber = client_numbers,
  transferValue = transfer_values
)


set.seed(789)
n <- nrow(transf)
dbank_numbers = sample(c("033", "421", "290", "666"), size = n, replace = TRUE)
dbank_branchs <- c(3321L, 4425L, 1979L, 8521L, 4078L, 9921L, 2231L, 6552L, 1200L, 1100L,
                   5420L, 6317L, 1002L, 8800L, 2400L)
dbank_branchs <- sample(dbank_branchs, size = n, replace = TRUE)
dbank_accounts <- sample(24561:86421, size = n)
dbank_accounts <- str_c(dbank_accounts, "-", sample(0:9,size = n, replace = TRUE))

client_country <- accounts$addressCountry
names(client_country) <- as.character(accounts$clientNumber)
countries <- client_country[as.character(transf$clientNumber)] %>% unname()
currencies <- c(
  "Netherlands" = "euro \U20AC",
  "United Kingdom" = "british pound \U00A3",
  "United States" = "dollar \U0024",
  "Amestris" = "zing \U0192"
)

transf <- transf %>% 
  arrange(datetimeTransfer) %>% 
  mutate(
    transferCurrency = currencies[countries] %>% unname(),
    transferID = as.character(seq_len(n) + 20221142),
    destinationBankNumber = dbank_numbers,
    destinationBankBranch = dbank_branchs,
    destinationBankAccount = dbank_accounts
  )


set.seed(888)
msgs <- c(
  "408 Request Timeout",
  "408 Request Timeout",
  "408 Request Timeout",
  "408 Request Timeout",
  "500 Server Unavailable",
  "500 Server Unavailable"
)
random_index <- sample(seq_len(n), size = length(msgs))
transf$transferLog <- NA_character_
transf$transferLog[random_index] <- msgs

transf <- transf %>% 
  select(
    1:6, transferLog,
    everything()
  )

write_delim(transf, "Data/transf.csv", delim = ";", na = "")
