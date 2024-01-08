FROM rstudio/r-base:4.2-focal
COPY . .
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y libfreetype6 fontconfig libfontconfig1-dev libfontconfig-dev libharfbuzz-dev libfribidi-dev libharfbuzz-dev libpng-dev libtiff5-dev libjpeg-dev
CMD ["Rscript", "art.R"]