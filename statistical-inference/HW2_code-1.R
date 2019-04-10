##################################################
### Exercise 1
##################################################


ncog <- read.table("transplant.txt")
names(ncog) <- c("t","type","d")
ncog$type<- factor(ncog$type)

# 2. 
library(survival)
library(ggfortify)
autoplot(survfit(Surv(t, d)~type,data=ncog))


# 3, 4
fit.exp <- survreg(Surv(t,d)~type, dist="exp",data=ncog)
summary(fit.exp)


# 5
fit<- survfit(Surv(t, d)~type,data=ncog)
par(mfrow=c(1,1))
plot(fit,col=c("darkred","darkgreen"),xlab="Months",conf.int=TRUE,main="Survival times")

x <- seq(from=0,to=70,by=1)
lines(x,1-pexp(x,exp(-coef(fit.exp)[1])),col="darkred")
lines(x,1-pexp(x,exp(-sum(coef(fit.exp)))),col="darkgreen")
legend(40, 1.1, legend=c("Type 1", "Type 2"), fill=c( "darkred","darkgreen"), cex=0.8)

#6
fit.wei <- survreg(Surv(t,d)~type,data=ncog)
summary(fit.wei)
2*(fit.wei$loglik[2]-fit.exp$loglik[2])
pchisq(2*(fit.wei$loglik[2]-fit.exp$loglik[2]),df = 1)


par(mfrow=c(1,1))
plot(fit,col=c("darkred","darkgreen"),xlab="Months",conf.int=TRUE,main="Survival times")

x <- seq(from=0,to=70,by=1)
lines(x,1-pexp(x,exp(-coef(fit.exp)[1])),col="darkred")
lines(x,1-pexp(x,exp(-sum(coef(fit.exp)))),col="darkgreen")
lines(x,1-pweibull(x,fit.wei$scale,exp(coef(fit.wei)[1])),lty=3,col="blue")
lines(x,1-pweibull(x,fit.wei$scale,exp(sum(coef(fit.wei)))),lty=4,col="blue")
legend(40, 1.1, legend=c("Type 1", "Type 2","Weibull fit"), fill=c("darkgreen", "darkred","blue"), cex=0.8)


##################################################
### Exercise 2
##################################################
library(boot)
library(mvdalab)
score = read.csv("scores.txt", sep = "")

cov1 = cov(score, use = "complete")

cov2 = cov(score, use = "pairwise")


mean_imputed = score
for(i in 1:ncol(mean_imputed)){
  mean_imputed[is.na(mean_imputed[,i]), i] <- mean(mean_imputed[,i], na.rm = TRUE)
}
cov3 = cov(mean_imputed)


df = score
mycov <- function(data, indices){
  datacopy = data[indices,]
  for(i in 1:ncol(datacopy)){
    datacopy[is.na(datacopy[,i]), i] <- mean(datacopy[,i], na.rm = TRUE)
  }
  return(cov(datacopy))
}
myBootstrap <- boot(df, mycov, R=1000)
m = matrix(0,5,5)
for(i in 1:1000){
  m = m + matrix(myBootstrap$t[i,], nrow = 5)
}
res = m/1000
cov4 = res


em = score
em_imputed_ob = imputeEM(em)
em_imputed = em_imputed_ob$Imputed.DataFrames[2][[1]]
cov5 = cov(em_imputed)
# 2

eigComp=eigen(cov1)
h.lambda=log(eigComp$values[1])
h.lambda-1.96*sqrt(2/22)
h.lambda+1.96*sqrt(2/22)


# 3
eigCov=eigen(cov(data(mathmarks)))
h.lambda=log(eigCov$values[1])
h.lambda-1.96*sqrt(2/88)
h.lambda+1.96*sqrt(2/88)


#########################################
### Exercise 3
#########################################

library(timeDate)
CentralPark <- read.csv("CentralPark.csv",header=T)
## Clean data
CP <- subset(CentralPark,select = c('DATE','PRCP'))
CP$DATE <- as.Date(CP$DATE, "%m/%d/%Y")
CP <- subset(CP, format.Date(DATE, "%m")=="07" )
CP.mc<- as.numeric(CP$PRCP>1.5)

## First-order model
N1 <- matrix(0,nrow = 2,ncol = 2)
for(i in 1:(length(CP.mc)-1)){ 
    if (i%%31 != 0){
    index1 <- as.numeric(CP.mc[i] == 1) + 1
    index2 <- as.numeric(CP.mc[i+1] == 1) + 1
    N1[index1,index2] = N1[index1,index2] + 1
    }
}

P1 <- N1/rowSums(N1)
P1

## significance
1-pnorm((P1[1,1]-P1[2,2])/(P1[1,1]*(1-P1[1,1])/(N1[1,1]+N1[1,2])+P1[2,2]*(1-P1[2,2])/(N1[2,1]+N1[2,2]))^0.5)

## Second-order model
N2 <- matrix(0,nrow = 4,ncol = 2)
for(i in 1:(length(CP.mc)-2)){ 
    if ((i%%31 != 0) & (i%%31 != 30)){
    index1 <- as.numeric(CP.mc[i] == 1) + 1 + 2*as.numeric(CP.mc[i+1] == 1)
    index2 <- as.numeric(CP.mc[i+2] == 1) + 1
    N2[index1,index2] = N2[index1,index2] + 1
    }
  }
P2 <- N2/rowSums(N2)
P2
## Likelihood Ratio Test
loglikihood1 <- sum(log(P1)*N1)
loglikihood2 <- sum(log(P2)*N2)
1-pchisq(2*(loglikihood2-loglikihood1),df = 2)

#########################################
### Exercise 4
#########################################

milk <- readxl::read_xls('milk.xls')
## 1
milk.linear <- data.frame(x = (1:nrow(milk)),y = milk$pounds)
fit.linear <- lm(y ~ x, data = milk.linear)
summary(fit.linear)
plot(x = (1:nrow(milk)), y = residuals(fit.linear),type = 'l')

milk.detrend <- residuals(fit.linear)
month <- rep(0,12)
for(i in 1:length(milk.detrend)){
  if (i%%12 != 0){
    month[i%%12] <- month[i%%12] + milk.detrend[i]
  }
  else {
    month[12] <- month[12] + milk.detrend[i]
  }
}
month <- month/(length(milk.detrend)/12)

milk.detrend <- milk.detrend - rep(month,(length(milk.detrend)/12))
## 2
acf(milk.detrend)
pacf(milk.detrend)
## 3
arima(milk.detrend, order = c(1,0,0))
arima(milk.detrend, order = c(2,0,0))
## 4

arima(milk.detrend, order = c(1,0,1))
arima(milk.detrend, order = c(1,0,2))


