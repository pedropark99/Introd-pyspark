if (!require("ggplot2")) {
  cat("[INFO]: ggplot2 not found! Installing ggplot2...\n")
  install.packages("ggplot2", repos = "https://vps.fmvz.usp.br/CRAN/")
}

if (!require("tibble")) {
  cat("[INFO]: tibble not found! Installing tibble...\n")
  install.packages("tibble", repos = "https://vps.fmvz.usp.br/CRAN/")
}

if (!require("dplyr")) {
  cat("[INFO]: dplyr not found! Installing dplyr...\n")
  install.packages("dplyr", repos = "https://vps.fmvz.usp.br/CRAN/")
}

if (!require("ragg")) {
  cat("[INFO]: ragg not found! Installing ragg\n")
  install.packages("ragg", repos = "https://vps.fmvz.usp.br/CRAN/")
}

library(ggplot2)
library(tibble)
library(dplyr)
library(ragg)

calc_x <- function(distance, angle, direction = 1L){
  distance * cos(angle) * direction
}

calc_y <- function(distance, angle, direction = 1L){
  distance * sin(angle) * direction
}

cover_main_color <- "#164E80"

colors <- c(
  "#d90429", "#ef233c",
  "#edf2f4", "#8d99ae",
  "#2b2d42"
)


set.seed(10)
range <- seq.default(0.1, 0.8, by = 0.1)
angles <- sample(range, size = 100, replace = TRUE)
df <- tibble(
    id = 1:100,
    x_start = runif(100),
    y_start = runif(100),
    distance = 10L,
    angle = angles,
    color = sample(colors, size = 100, replace = TRUE),
    direction = 1L#sample(c(1L, -1L), size = 100, replace = TRUE)
  ) %>% 
  mutate(
    x_end = calc_x(distance, angle, direction) + x_start,
    y_end = calc_y(distance, angle, direction) + y_start
  )


ggplot(df) +
  geom_point(
    aes(x = x_start, y = y_start)
  )


pl <- ggplot(df) +
  geom_segment(
    aes(x = x_start, y = y_start, xend = x_end, yend = y_end, group = id, color = color)
  ) +
  theme_void() +
  scale_color_identity()


agg_png(
  "Cover/Images/lines.png", res = 800, 
  width = 4500, height = 4500, background = NULL
)
print(pl)
dev.off()


