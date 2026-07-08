#%%

library('MatchIt')
library('tidyverse')

sero_pvi <- read.csv("~/Downloads/Frame for R.csv")
pvi_only <- read.csv("~/Downloads/PVI Only.csv")

#%%
exclusions <- c('Sample ID', 'race', 'apollo', 'covid_total_vaccine_doses', 'covid_total_infections', 'covid_prior', 'vaxxed', 'vaxxed_days', 'Spike titer','covid_infection')

sero_pvi = sero_pvi |> mutate(sex = if_else(sex == 1, "Male", "Female")) 

m.out <- matchit(PVI ~ age + sex + race_ordinal + covid_infection + vaccinated, data = sero_pvi, 
        distance = "scaled_euclidean", replace = FALSE, ratio = 2)

#%%

summary(m.out)

plot(summary(m.out), xlim=c(0,1.5))

#%%

matched <- match.data(m.out)

write.csv(matched, "~/Downloads/Matched Data R.csv", row.names = FALSE)

#%%

colnames(pvi_only)

m2.out <- matchit(Apollo ~ Age.at.Baseline + Sex + COVID.Total.Immune.Events + Flu.Total.Immune.Events + African.American + 
        Asian + Hispanic.Latino+ White + Middle.Eastern.North.African + Native.American.Alaska.Native +
       Multi.racial, data = pvi_only, distance = "scaled_euclidean", replace = TRUE, ratio = 5)

summary(m2.out)

plot(summary(m2.out), xlim=c(0,2))

matched2 <- match.data(m2.out)
matchs2 <- get_matches(m2.out, "all")

write.csv(matched2, "~/Downloads/Matched Data PVI Only.csv", row.names = FALSE)
write.csv(matchs2, "~/Downloads/Matches PVI Only.csv", row.names = FALSE)
