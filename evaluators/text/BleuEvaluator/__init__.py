from jina.executors.evaluators.text import BaseTextEvaluator

class BleuEvaluator(BaseTextEvaluator):
    """
    :class:`BleuEvaluator`Bilingual Evaluation Understudy Score. 
    Evaluates the generated sentence (actual) against a desired sentence. 
    It will use the Bleu on NLTK package.
    A perfect match will score 1.0 and a complete mismatch will score 0.0

    The NLTK library can score n-gram individually or cummulative.
    Here we use the cumulative as it is more precise.
    https://machinelearningmastery.com/calculate-bleu-score-for-text-python/

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    @staticmethod
    def get_score(desired_list, actual_list, n_gram):
        '''
        Cumulative score is the calculation of individual n-grams
        from 1 to n-order, and then weights them with the geometric mean
        - desired_list, actual_list: are the sentences to be scored
        It will check the biggest n-gram possible, if the n-gram is smaller than 4, 
        which is the standard for NLTK, it is neccesary to reset the weights
        '''
        import nltk.translate.bleu_score as bleu    
        from nltk.translate.bleu_score import SmoothingFunction

        if n_gram == 1:
            return bleu.sentence_bleu(desired_list, actual_list, weights = (1.0, 0, 0, 0), smoothing_function=SmoothingFunction().method4)
        elif n_gram == 2:
            return bleu.sentence_bleu(desired_list, actual_list, weights = (0.5, 0.5, 0, 0), smoothing_function=SmoothingFunction().method4)
        elif n_gram == 3:
            return bleu.sentence_bleu(desired_list, actual_list, weights = (0.33, 0.33, 0.33, 0), smoothing_function=SmoothingFunction().method4)
        else:
            return bleu.sentence_bleu(desired_list, actual_list) #if the ngram is at least 4, use the standard 
        

    def evaluate(self,
            actual,
            desired,
            *args,
            **kwargs) -> float:
        """"
        :param desired: the expected text given by user as groundtruth.
        :param actual: the text predicted by the search system.
        :return the evaluation metric value for the request document.

        NLTK expectes an array of strings, 
        so the incoming string needs to be tokenized first.
        They will be stored in a desired_list and actual_list accordingly
        """

        # set everything to undercase and tokenize
        desired_list = desired.lower().split()
        actual_list = actual.lower().split()
        return self.get_score([desired_list], actual_list, len([desired_list]))

