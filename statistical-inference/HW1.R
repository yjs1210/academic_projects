library(dplyr)
library(data.table)
library(readr)
library(lubridate)
library(zoo)
library(ggplot2)
library(tidyr)
library(broom)

df= read.delim("/Users/James/AnacondaProjects/academic_projects/statistical-inference/kidney.txt",sep=" ", header=TRUE)
df = separate(df, 'age.tot',sep= " ", into = c('age','tot'))
df$age <- as.integer(df$age)
df$tot <- as.numeric(df$tot)

ggplot(data=df, aes(x=age, y=tot)) + geom_point() 

fit <- lm(data=df, tot~age)

Sxx <- sum((df$age - mean(df$age))^2)
Sxy <- sum((df$age - mean(df$age))*(df$tot - mean(df$tot)))
Syy <- sum((df$tot - mean(df$tot))^2)

B <- Sxy/Sxx
A<- mean(df$tot)  - B*mean(df$age)

SSr = (Sxx*Syy - Sxy^2) / Sxx
n=nrow(df)

##5
Bt = sqrt((n-2)*Sxx/SSr)*(B)
At = sqrt(n*(n-2)*Sxx/SSr/sum(df$age^2))*(A)
PBt = pt(Bt,n-2, lower=FALSE)
PAt = pt(At,n-2,lower=FALSE)


##7, seems reasonable
predict(fit,newdata=data.frame(age=100))


##8, Yes reasonably iid
resid <- augment(fit)
ggplot(resid, aes(x=.fitted, y=.resid)) + geom_point() 

##9. 

