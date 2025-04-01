# Basic Models

## Support Vector Machine(SVM)

- Classifies data by finding an optimal line or hyperplane that maximizes the distance between each class in an N-dimensional space
- When the data is not linearly separable, kernel functions are used to transform the data higher-dimensional space to enable linear separation (called kernel trick)

### Different types:
- Linear SVMs
- Nonlinear SVMs
- Support vector regression

### Advantages:

- Effective in high dimensional spaces

- Still effective in cases where number of dimensions is greater than the number of samples

- Uses a subset of training points in the decision function (called support vectors), so it is also memory efficient

- Versatile: different Kernel functions can be specified for the decision function. Common kernels are provided, but it is also possible to specify custom kernels.


### Disadvantages:

- If the number of features is much greater than the number of samples, avoid over-fitting in choosing Kernel functions and regularization term is crucial

- SVMs do not directly provide probability estimates, these are calculated using an expensive five-fold cross-validation


## Naive Bayes
- Probabilistic classifier based on Bayes' Theorem
- Unlike discriminative classifiers, like logistic regression, it does not learn which features are most important to differentiate between classes

- Bayes’ Theorem is distinguished by its use of sequential events, where additional information later acquired impacts the initial probability <br> 
- The prior probability is the initial probability of an event before it is contextualized under a certain condition, or the marginal probability <br>
- The posterior probability is the probability of an event after observing a piece of data

![Bild Bayes](https://www.ibm.com/content/dam/connectedassets-adobe-cms/worldwide-content/cdp/cf/ul/g/9f/c8/Naive_Bayes_Formula.png)

### Types of Bayes Classifiers
- Gaussian Naïve Bayes (GaussianNB): used with Gaussian distributions and continuous variables
- Multinomial Naïve Bayes (MultinomialNB): assumes that the features are from multinomial distributions. This variant is useful when using discrete data (like in natural language processing tasks)

- Bernoulli Naïve Bayes (BernoulliNB): is used with Boolean variables

### Advantages

- Less complex: Compared to other classifiers, Naïve Bayes is considered a simpler classifier since the parameters are easier to estimate. As a result, it’s one of the first algorithms learned within data science and machine learning courses.

- Scales well: Compared to logistic regression, Naïve Bayes is considered a fast and efficient classifier that is fairly accurate when the conditional independence assumption holds. It also has low storage requirements.
- Can handle high-dimensional data: Use cases, such document classification, can have a high number of dimensions, which can be difficult for other classifiers to manage.


### Disadvantages:

- Subject to Zero frequency: Zero frequency occurs when a categorical variable does not exist within the training set. For example, imagine that we’re trying to find the maximum likelihood estimator for the word, “sir” given class “spam”, but the word, “sir” doesn’t exist in the training data. The probability in this case would zero, and since this classifier multiplies all the conditional probabilities together, this also means that posterior probability will be zero. To avoid this issue, laplace smoothing can be leveraged.

- Unrealistic core assumption: While the conditional independence assumption overall performs well, the assumption does not always hold, leading to incorrect classifications.



## SVM vs naive Bayes
Both Naive Bayes and SVM classifies are commonly used for text classification tasks. SVMs tend to perform better than Naive Bayes when the data is not linearly separable.