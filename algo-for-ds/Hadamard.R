test =matrix(1,nrow=1,ncol=1)
test2 =matrix(1,nrow=1,ncol=1)




Hadamard =matrix(c(1,1,1,-1),nrow=2,ncol=2)

Hadamard2=rbind(cbind(Hadamard,Hadamard),cbind(Hadamard,-Hadamard))
Hadamard3=rbind(cbind(Hadamard2,Hadamard2),cbind(Hadamard2,-Hadamard2))
vector2 = 1:4
vector3 = 1:8

Hadamard3 %*% vector


sumproduct <- function(matrix,vector){
  mid <- ncol(matrix)/2
  if(length(matrix)==1){
    return(vector*matrix)
  }else{
    top <- sumproduct(matrix[1:mid,1:mid],vector[1:mid])
    bottom <- sumproduct(matrix[1:mid,(mid+1):(mid*2)],vector[(mid+1):(mid*2)])
    return(matrix(c(top+bottom,top-bottom),nrow=mid,ncol=1))
  }
} 


