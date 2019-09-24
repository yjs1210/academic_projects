df<-read.table('/Users/james/AnacondaProjects/academic_projects/statistical-inference/cigarettes.txt', header = TRUE)
library(mgcv)
fit_gam <- gam(cigs ~ educ+s(cigpric)+white+s(age)+s(income)+restaurn, data=df,family =poisson)
summary(fit_gam)
plot(fit_gam)

fit_gam$coefficients

summary(lm(cigs~., data=df))

head(df)

predict(fit_gam, newdata = data.frame(educ=12,cigpric=40,white=1,age=50,income=10000,cigs=3,restaurn=0))
predict(fit_gam, newdata = data.frame(educ=12,cigpric=60,white=1,age=50,income=10000,cigs=3,restaurn=0))
