library(igraph)
library(ggplot2)
options(scipen = 999)
options(rgl.useNULL = TRUE)
library(rgl)
library(export)
library(reshape2)

# Create the data
data <- data.frame(
  Group = rep(c(0.2, 0.4, 0.6, 0.8), each=2),
  Algorithm = rep(c("vanilla peeling", "k-core"), 4),
  Followers = c(30245.338520288467, 1051.5250821113586, 8866.438943386078, 21.118804216384888, 8941.41350889206, 9.618403434753418, 8802.479057073593, 10.06099796295166),
  Time = c("8108", "1439", "343", "99")
)

# Apply log10 transformation
data$LogFollowers <- log10(data$Followers)

# Create the bar plot with y-axis in log scale
plot <- ggplot(data, aes(x = factor(Group), y = LogFollowers, fill = Algorithm)) +
  geom_bar(stat = "identity", position = position_dodge()) +
  scale_fill_manual(values = c("grey", "black")) +
  labs(x = "b", y = "run-time sec (log scale)", title = "brightkite") +
  scale_y_continuous(breaks = c(0, 1, 2, 3, 4, 5), labels = 10^c(0, 1, 2, 3, 4, 5)) +
  theme_minimal() +
  geom_text(aes(label = Time, y = LogFollowers + 0.1), 
            position = position_dodge(width = 0.9), 
            size = 3)

# Display the plot
print(plot)

# Save the plot
graph2ppt(file = "k_core_BK", width = 7, height = 5)
