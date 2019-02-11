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
###CI assuming normal
width = sqrt(SSr/((n-2)*Sxx))*qt(0.025,nrow(df)-2,lower.tail = FALSE)
B - width
B + width

###Not assuming normal??

###10.
out <- c()
for (i in 1:1000){
  sam <-df[sample(nrow(df),replace=TRUE),]
  Sxx_sam <- sum((sam$age - mean(sam$age))^2)
  Sxy_sam <- sum((sam$age - mean(sam$age))*(sam$tot - mean(sam$tot)))
  B_sam <- Sxy_sam/Sxx_sam
  out = c(out,B_sam)
}
quantile(out,c(.025,.975))

###pretty close but it seems the tails are fatter than what the distribution models. Width of the interva lis wider with bootstrap

11. 

calc_corr <- function (df){
  cov = sum((df$age - mean(df$age))*(df$tot - mean(df$tot)))/(nrow(df)-1)
  correlation = cov/sd(df$age)/sd(df$tot)
  return(correlation) 
}

bench <- calc_corr(df)

out_corr<- c()
for (i in 1:nrow(df)){
  df_temp <- df[-i,]
  out_corr <- c(out_corr,calc_corr(df_temp))
}

diff <- out_corr - bench
idx<-which.max(abs(diff))
diff[157]
diff[57]
df[idx,]




##### QUestions 3.
df_merton = data.frame(x=c(2,3,4,5,6,7,8,9),frequency=c(179,51,17,6,8,1,0,2))
u = c(seq(.1,3,by=.1))
log(u)

likelihood = c()
for (i in 1:length(u)){
  mu = u[i]
  klogmu = sum(log(mu)*df_merton$x*df_merton$frequency)
  summ = sum(factorial(df_merton$x)*df_merton$frequency)
  n= sum(df_merton$frequency)
  constant1 = n*mu
  constant2 = n*(1-exp(-mu)-mu*exp(-mu))
  fin = klogmu - constant1 - constant2 - summ 
  likelihood = c(likelihood,fin)
}

df_plot = data.frame(mu=u,likelihood=likelihood)
ggplot(data=df_plot, aes(x=mu, y=likelihood)) + geom_line() 


##6
df_merton = data.frame(x=c(2,3,4,5,6,7,8,9),frequency=c(179,51,17,6,8,1,0,2))
u = c(seq(.1,3,by=.001))
log(u)

likelihood = c()
for (i in 1:length(u)){
  mu = u[i]
  klogmu = sum(log(mu)*df_merton$x*df_merton$frequency)
  summ = sum(factorial(df_merton$x)*df_merton$frequency)
  n= sum(df_merton$frequency)
  constant1 = n*mu
  constant2 = n*(1-exp(-mu)-mu*exp(-mu))
  fin = klogmu - constant1 - constant2 - summ 
  likelihood = c(likelihood,fin)
}

df_plot = data.frame(mu=u,likelihood=likelihood)
ggplot(data=df_plot, aes(x=mu, y=likelihood)) + geom_line() 

u_mle = u[which.max(likelihood)]


var_mle = 1/(n + u_mle*2*n*exp(-u_mle) - u_mle^2*n*exp(-u_mle))

##3.8 CI
u_mle - 1.96/sqrt(n)*sqrt(var_mle)
u_mle + 1.96/sqrt(n)*sqrt(var_mle)


#3.9 
Ey= u_mle*(1-exp(-u_mle)) / (1-exp(-u_mle)-u_mle*exp(-u_mle))
