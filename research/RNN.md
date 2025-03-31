# RNN: Recurrent neural network

> Links: [ibm video: What is a RNN?](https://www.youtube.com/watch?v=Gafjk7_w1i8), [instruction how to implement RNN](https://www.geeksforgeeks.org/rnn-for-text-classifications-in-nlp/)

#### Why RNN?
RNNs are particularly good at evaluating the contextual links between words in NLP text classification, which helps them identify patterns and semantics that are essential for correctly classifying textual information. 

**Main feature of RNN:** 
- Loops & memory > they can remember previous inputs from previous steps, with that, they can analyze context in data
-  same weight parameter within each layer of the network (but still updated via gradient and backpropagation!)

![Feedforward vs recurrent neural networks](https://www.ibm.com/content/dam/connectedassets-adobe-cms/worldwide-content/cdp/cf/ul/g/27/80/what-are-recurrent-neural-networks-combined.jpg)


**different kind of RNNs:**
- sequence-to-sequence network: sequence of input > RNN > produces sequence of outputs (time series)
- sequence-to-vector network: sequence of input > RNN > one final output (sentiment analyses)
- weight of the xx : single input > RNN >sequence of outputs (image to text)
- encoder-decoder-architecture: sequence of input > encoder > Vector > Decoder > sequence of output (language translation)

**Key challenges:**
- vanishing/exploding gradients: too small/large updates during backpropagation (gradient, weights) > LSTM (Long Short-Term Mermory), GRU (Gated Recurrent Units)
- complexity in training: high computational power & time needed (> _check text length?_)

**common activation functions**
- Sigmoid
- The Tanh (Hyperbolic Tangend) Function
- ReLu

![Activation functions](https://www.ibm.com/content/dam/connectedassets-adobe-cms/worldwide-content/creative-assets/s-migr/ul/g/13/0d/two-dimensional-coordinate-system.png)


RNN use has declined in artificial intelligence, especially in favor of architectures such as transformer models, but RNNs are not obsolete. RNNs were traditionally popular for sequential data processing (for example, time series and language modeling) because of their ability to handle temporal dependencies.

However, RNNs’ weakness to the vanishing and exploding gradient problems, along with the rise of transformer models such as BERT and GPT have resulted in this decline. Transformers can capture long-range dependencies much more effectively, are easier to parallelize and perform better on tasks such as NLP, speech recognition and time-series forecasting.

That said, RNNs are still used in specific contexts where their sequential nature and memory mechanism can be useful, especially in smaller, resource-constrained environments or for tasks where data processing benefits from step-by-step recurrence.

**Implementation**
- [Keras](https://www.tensorflow.org/guide/keras/working_with_rnns)