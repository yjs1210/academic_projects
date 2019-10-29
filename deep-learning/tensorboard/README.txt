3.1 Activation Functions
Please refer to the plot 3.1,ActivatinFunctionsAccuracies.PNG.
Here we notice a few things, built-in Relu has the best performance in the test set in terms of accuracy followed by Relu that we implemented then Tanh and Sigmoid. Our Relu seems to underperform the built-in Relu ever so slightly probably because there are some optimisations done within Tensorflow. All in all, outperformance of Relu functions make sense since Relu is thought to be the better optimisation function largely because of its ability to be resistant to gradient vanishing, and also because its constant gradient allows faster learning. 

Tanh function performing better than sigmoid makes sense since sigmoid function's derivative maxes out at .25 while it maxes out at 1 for tanh.
This means that, algorithm can make updates on the variables much faster with the tanh function than the sigmoid function. 


3.2.a Optimizer
Please refer to diagram 3.2OptimizerAccuracies.PNG. 
We first observe that Adam converges the fastest, achieving very high accuracy right from the early epochs. SGD soon catches up. Adadelta however doesn't seem to perform well.
Adam is considered to be an optimiszr that converges fast and is efficient while SGD is an optimizer that is slower but believed to generalize better(https://arxiv.org/abs/1705.08292). This is apparent in our findings here because SGD slowly catches up to Adam. It is possible that with the right parameter tuning and enough epochs that SGD may have started outperforming Adam.

Adadelta performing the worst makes sense since it is thought to be the solver that works well with sparse data such as NLP and TFIDF problems because it penalises parameters that update frequently, and therefore emphasises information that is not as frequent. So in our case, this is not a great solver, and it shows in our plots.

Last thing to point out is that SGD with higher momentum performs better than SGD with no momentum. This is because momentum hyperparamter accelerates SGD in the relevant direction and dampens oscillations. So this higher momentum is helping us converge faster to the optimum. 

3.2.b. Initialization
Please refer to the 3.2b.IntiailizationAuccracies.PNG
We try three different initialization settings, ones, zeros and GlorotUniform. We see that GlorotUniform clearly outperforms the other two. This can be due to couple of reasons.
In general, it is not a good idea to initalize the NN weights with equal constants. First, the network can get stuck in a local minima because error is back propagated proportion to the values of the weights. By giving lots of different values, it is less likely to get stuck in a local minima and gives us a better chance of finding the global minimum. 

Additionally, when neurons all start with the same weights, then they all follow the same gradient. Which means that they cannot learn different things at the same time. This makes
them less optimal. 

Last two points help us explain why GlorotUniform works the best. It samples from a uniform distribution within [-limit, limit] where limit is sqrt(6 / (fan_in + fan_out))
where fan_in is the number of input units in the weight tensor and fan_out is the number of output units in the weight tensor. So it basically ensures that there is sufficient randomness in our weights and that they come from a reasonably limited range of numbers. Therefore, it gets around the two issues that we just discussed. 


3.3. Extra Credit
Common activation functions such as sigmoid or tanh suffer from the vanishing gradient problem because they squash their input into a very small output range. Therefore, even a large change in input range lead to a small change in the output. We can make this problem worse by having many layers all of which use sigmoid or tanh activation functions. We can solve this by using a relu activation instead since it's output's gradient is either 0 or 1, and therefore never vanishes.

Please refer to the 3.3ExtraCreditActivationFiunctionAccuracies.PNG. In this example we purposefully build two very deep NNs with 10 dense layers each. One of them uses only the sigmoid activation function while the other uses relu activation function. We can see that sigmoid function stops learning after epoch 2 because of the vanishing gradient, which becomes a larger problem as the network gets deeper. We can simply solve this by using a Relu activation function. As you can see in the plot, the only thing that has changed is the activation function but we were able to escape getting stuck in a local optimum. Again, this is because Relu has a constant gradient and does not suffer from the vanishing gradient problem.

Taking a look at the histograms(3.3ExtraCreditReluHistogram, 3.3ExtraCreditTanhHistogram) we can see that the distribution of the activations are more varied in the Relu layer than the Sigmoid layer. There is more jaggedness that changes over epochs whereas Sigmoid layer is just frozen. Third layers of the network was chosen to portray because they looked the most interesting. Sigmoid distribution basically looks the same across all epochs to a human eye while there is a lot of variability in Relu. If we were to plot gradients, it's likely we will observe a very small gradient for the Sigmoid while that would not be the case for Relu. 


Taking a look at the gradients(3.3ExtraCreditGradientsUsingRelu, 3.3ExtraCreditGradientUsingSigmoid), the plot shows the average gradient of the layer variables of the second layers of both networks. We can see that the gradients of Relu actually increases in value over epoch whereas it marches towards zero for sigmoid. This demonstrates the vanishing gradient problem and also confirms our previous hypothesis given the histogram of the activations which wasn't changing much for sigmoid but was changing for Relu. 


