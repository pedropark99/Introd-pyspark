

a <- tibble::tibble(
  dateOfEvent = c("15/06/2022"),
  timeOfEvent = c("15/06/2022 14:33:10", "15/06/2022 14:40:08", "15/06/2022 15:48:41"),
  userId = uuid::UUIDgenerate(n = 1),
  nameOfEvent = c("entry", "click: shop", "select: payment-method")
)


jsonlite::write_json(a, "Data/user-events.json")
