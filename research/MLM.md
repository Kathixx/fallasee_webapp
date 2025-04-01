## Masked Language Modeling
**A pretraining strategy** (not a model on its own) used in models like BERT.

- During training, some tokens in the input are replaced with [MASK], and the model tries to predict them.

- What’s cool about language modeling tasks is you don’t need labels (also known as an unsupervised task) because the next word is the label.
- Bidirectional context understanding — it looks at both left and right context of a token.

Once you have the data, you need to:

- preprocess
- tokenize
- train
- evaluate
- use it for inference

**Masked language modeling (MLM)**: taking a sentence, the model randomly masks 15% of the words in the input then run the entire masked sentence through the model and has to predict the masked words. This is different from traditional recurrent neural networks (RNNs) that usually see the words one after the other, or from autoregressive models like GPT which internally masks the future tokens. It allows the model to learn a bidirectional representation of the sentence.

**Next sentence prediction (NSP)**: the models concatenates two masked sentences as inputs during pretraining. Sometimes they correspond to sentences that were next to each other in the original text, sometimes not. The model then has to predict if the two sentences were following each other or not. (This paragraph is in the hugging face page for bert-base-uncased)

[Masked language modeling in huggingface.](https://huggingface.co/docs/transformers/main/en/tasks/masked_language_modeling#preprocess)

[This chapter](https://web.stanford.edu/~jurafsky/slp3/11.pdf) of the book Speech and Language Processing has a clear explanation about MLMs.

[This Medium article](https://medium.com/data-science/understanding-masked-language-models-mlm-and-causal-language-models-clm-in-nlp-194c15f56a5#:~:text=MLM%20loss%20is%20preferred%20when,system%20that%20generates%20fluent%20text%20.) has visuals and examples.