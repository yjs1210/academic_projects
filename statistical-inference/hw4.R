df<-read.table('/Users/james.lee/AnacondaProjects/academic_projects/statistical-inference/cigarettes.txt', header = TRUE)
library(mgcv)
fit_gam <- gam(cigs ~ educ+s(cigpric)+white+s(age)+s(income)+restaurn, data=df)
summary(fit_gam)


summary(lm(cigs~., data=df))
