from abc import ABC, abstractmethod

class Transformer(ABC):
    """
    Abstract base class for modules that take in a Corpus and modify the Corpus
    and/or extend it with additional information, imitating the scikit-learn
    Transformer API. Exposes fit() and transform() methods. fit() performs any
    necessary precomputation (or “training” in machine learning parlance) while
    transform() does the work of actually computing the modification and
    applying it to the corpus. All subclasses must implement transform();
    subclasses that require precomputation should also override fit(), which by
    default does nothing. Additionally, the interface also exposes a
    fit_transform() method that does both steps on the same Corpus in one line.
    By default this is implemented to simply call fit() followed by transform(),
    but designers of Transformer subclasses may also choose to overwrite the
    default implementation in cases where the combined operation can be
    implemented more efficiently than doing the steps separately.
    """

    def fit(self, corpus):
        """Use the provided Corpus to perform any precomputations necessary to
        later perform the actual transformation step.

        :param corpus: the Corpus to use for fitting
        
        :return: the fitted Transformer
        """
        return self

    @abstractmethod
    def transform(self, corpus):
        """Modify the provided corpus. This is an abstract method that must be
        implemented by any Transformer subclass

        :param corpus: the Corpus to transform

        :return: modified version of the input Corpus. Note that like the 
            scikit-learn equivalent, transform() is not meant to be an inplace 
            operation.
        """
        pass

    def fit_transform(self, corpus):
        """Fit and run the Transformer on a single Corpus.

        :param corpus: the Corpus to use

        :return: same as transform
        """
        self.fit(corpus)
        return self.transform(corpus)