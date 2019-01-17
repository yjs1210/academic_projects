######Load Data####
dat = read.csv("spam.csv", header = TRUE)
my_data <- read.delim("http://www.sthda.com/upload/boxplot_format.txt")
my_data <- read.delim("mtcars.txt")

#####Create some dataframe#####

comp<-c(1,1,1,1,1,1,2,2,2,2)
yr <- c(1998,1999,2000,2001,2002,2003,2004,2005,2006)
q1<- runif(i,min=0,max=100)
df <- data.frame(com=comp,year=yr,Qtr1=q1)


#####Cleaning & Joining Data#####
df.m[is.na(df.m)] <- 0



##Apply functions, on each element
result <- sapply(v,function(num){num*2})
sapply(v,add_choice,choice=100)

##For row wise operations, 
use apply(df,1,function,args=any)
##for column wise operations, 
use apply(df,2,function,args=any)

##Rowwise apply
iris %>% 
  rowwise() %>% 
  mutate(Max.Len= max(Sepal.Length,Petal.Length))

#Types
as.data.frame(v)

#Append
append(v,v2)
as.data.frame(v)
rbind(df,df1)

##Joins
use dplyr inner_join, left_join...

###Split, train test
library(caret)


##############EDA Analysis, cut ,slice##########
import(dplyr)

##groups, you wanna call group by then summarise(min,max,mean,emdian,sum,sd,iqr,n(number of obs),n_distinct(),nth)
mtcars %>% group_by(am) %>% summarise(mpg_by_trans = mean(mpg))

##Window functions, you want to use mutate to add the column onto DF
#duplicate treatment: 1,1,3
mutate(players, G_rank = min(rank(desc(G))))

#duplciate treatement 1,1,2
mtcars %>% mutate(dense_rank(desc(mpg))) %>% arrange(desc(mpg))
#1,2,3
mtcars %>% mutate(row_number(desc(mpg))) %>% arrange

##other windows, percent_rank(), cume_dist(), ntile(), lag(),lead(),cumsum(),cumprod()

##rolling cumsum
library(zoo)

as.data.frame(mtcars %>% arrange(am,desc(mpg)) %>% group_by(am)%>%
                mutate(cum_rolling10 = rollapplyr(mpg, width = 10, FUN = sum, partial = TRUE))
              %>% arrange(am,desc(mpg)) 
)

##rowwise apply
##Rowwise apply
iris %>% 
  rowwise() %>% 
  mutate(Max.Len= max(Sepal.Length,Petal.Length))

##Other dplyr commands
filter() and slice()
arrange(desc(airtime))
select() and rename(airlines_carrier=carrier,)
distinct()
mutate() and transmute()
summarise()
sample_n() and sample_frac(df,.5)
