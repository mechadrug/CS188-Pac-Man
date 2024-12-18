import nn
class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** YOUR CODE HERE ***"
        return nn.DotProduct(x,self.w)
        
        

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        "*** YOUR CODE HERE ***"
        if nn.as_scalar(self.run(x))>=0:
            return 1
        return-1

    def train(self, dataset):
        """
        Train the perceptron until convergence.
        """
        "*** YOUR CODE HERE ***"
        
        while True:
            mistake=0
            batch_size=1
            for x,y in dataset.iterate_once(batch_size):
                score=self.get_prediction(x)
                label=nn.as_scalar(y)
                if score!=label:
                    self.w.update(nn.Constant(nn.as_scalar(y)*x.data),1)
                    mistake+=1
            if mistake==0:
                break


class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.w1=nn.Parameter(1,64)
        self.w2=nn.Parameter(64,8)
        self.w3=nn.Parameter(8,1)
        self.b1=nn.Parameter(1,64)
        self.b2=nn.Parameter(1,8)
        self.b3=nn.Parameter(1,1)

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"
        #x:m*1,则对应的参数self.w应该是1*n,最终应该返回一个m*1的y,y和x的格式相同
        #h1=f1(x)=f1(x*self.w1+b1)=[x.x,self.w1.y]
        #h2=f2(h1)=f2(h1*self.w2+b2)=[h1.x,self.w1.y]
        #y^=f3(h2)=h2*self.w3+b3=[h2.x,self.w3.y]
        #x:32*1
        #self.w1:1*64
        #h1:32*64
        #self.w2:64*8?1?4?
        #h2:32*8
        #self.w3:8*1
        #h3:32*1=y^
        #返回模型预测,用到:
        #nn.ReLU->f
        #nn.Linear(x,t)->*
        #nn.AddBias->+
        h1=nn.ReLU(nn.AddBias(nn.Linear(x,self.w1),self.b1))
        h2=nn.ReLU(nn.AddBias(nn.Linear(h1,self.w2),self.b2))
        h3=nn.AddBias(nn.Linear(h2,self.w3),self.b3)
        return h3
    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        #nn.SquareLoss 返回y和y^的差值
        return nn.SquareLoss(self.run(x),y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        batchsize=20
        loss=float('inf')
        while loss>=0.01:
            for x,y in dataset.iterate_once(batchsize):
                lossX=self.get_loss(x,y)
                loss=nn.as_scalar(lossX)
                print(loss)
                s=[self.w1,self.w2,self.w3,self.b1,self.b2,self.b3]
                t=nn.gradients(lossX,s)
                for i in range(len(s)):
                    s[i].update(t[i],-0.001)
                

        #当差值大于0.01就继续训练
        #训练过程:计算训练损失;self.get_loss
        #获取损失梯度;nn.gradients
        #对每一个参数基于梯度进行更新对于参数i调用i.update(i梯度,学习率)


class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.w1=nn.Parameter(784,128)
        self.w2=nn.Parameter(128,32)
        self.w3=nn.Parameter(32,10)
        self.b1=nn.Parameter(1,128)
        self.b2=nn.Parameter(1,32)
        self.b3=nn.Parameter(1,10)

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        h1=nn.ReLU(nn.AddBias(nn.Linear(x,self.w1),self.b1))
        h2=nn.ReLU(nn.AddBias(nn.Linear(h1,self.w2),self.b2))
        h3=nn.AddBias(nn.Linear(h2,self.w3),self.b3)
        return h3

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SoftmaxLoss(self.run(x),y)


    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        batchsize=100
        best_val_accuracy=0
        race=0.1
        loss=float('inf')
        while best_val_accuracy<=0.98:
            for x,y in dataset.iterate_once(batchsize):
                lossX=self.get_loss(x,y)
                loss=nn.as_scalar(lossX)
                print(loss)
                s=[self.w1,self.w2,self.w3,self.b1,self.b2,self.b3]
                t=nn.gradients(lossX,s)
                for i in range(len(s)):
                    s[i].update(t[i],-race)
            best_val_accuracy=dataset.get_validation_accuracy()
            

            



class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]

        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"

    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"

    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
