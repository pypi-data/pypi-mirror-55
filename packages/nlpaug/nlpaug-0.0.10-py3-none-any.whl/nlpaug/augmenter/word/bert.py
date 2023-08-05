"""
    Augmenter that apply BERT's based operation to textual input.
"""

from nlpaug.augmenter.word import WordAugmenter
from nlpaug.util import Action
import nlpaug.model.lang_models as nml
from nlpaug.util.decorator.deprecation import deprecated

BERT_MODEL = {}


def init_bert_model_deprecated(model_path, device, tokenizer_path, force_reload=False):
    # Load model once at runtime

    global BERT_MODEL
    if BERT_MODEL and not force_reload:
        return BERT_MODEL

    bert_model = nml.BertDeprecated(model_path, tokenizer_path, device)
    bert_model.model.eval()
    BERT_MODEL = bert_model

    return bert_model


@deprecated(deprecate_from='0.0.8', deprecate_to='0.0.10', msg="Use ContextualWordEmbsAug from 0.0.8 version")
class BertAug(WordAugmenter):
    """
    Augmenter that leverage BERT's embeddings to find top n similar word for augmentation.

    :param str model_path: Model name or model path. It used transformers to load the model.
    :param str tokenizer_path: Tokenizer name of path. It used transformers to load the tokenizer.
    :param str action: Either 'insert or 'substitute'. If value is 'insert', a new word will be injected to random
        position according to contextual word embeddings calculation. If value is 'substitute', word will be replaced
        according to contextual embeddings calculation
    :param int aug_min: Minimum number of word will be augmented.
    :param float aug_p: Percentage of word will be augmented.
    :param int aug_n: Top n similar word for lucky draw
    :param list stopwords: List of words which will be skipped from augment operation.
    :param device: Use either cpu or gpu. Default value is 'cpu' while possible values are 'cuda' and 'cpu'.
    :param str name: Name of this augmenter

    >>> import nlpaug.augmenter.word as naw
    >>> aug = naw.BertAug()
    """

    def __init__(self, model_path='bert-base-uncased', tokenizer_path='bert-base-uncased', action=Action.SUBSTITUTE,
                 name='Bert_Aug', aug_min=1, aug_p=0.3, aug_n=5, stopwords=None, device='cpu', verbose=0):
        super().__init__(
            action=action, name=name, aug_p=aug_p, aug_min=aug_min, tokenizer=None, stopwords=stopwords,
            verbose=verbose)
        self.model_path = model_path
        self.tokenizer_path = tokenizer_path
        self.aug_n = aug_n
        self.device = device
        self.model = self.get_model(device=device, force_reload=False)
        self.tokenizer = self.model.tokenizer.tokenize
        self.reverse_tokenizer = self._reverse_tokenizer

    def skip_aug(self, token_idxes, tokens):
        results = []
        for token_idx in token_idxes:
            # Some token is not a partial word.
            word = tokens[token_idx]

            if word[:2] != nml.Bert.SUBWORD_PREFIX:
                results.append(token_idx)

        return results

    def _reverse_tokenizer(self, tokens):
        result = ''
        for token in tokens:
            if token[:2] == nml.Bert.SUBWORD_PREFIX:
                result += token[2:]
            else:
                result += ' ' + token
        return result[1:]

    def insert(self, data):
        tokens = self.tokenizer(data)
        results = tokens.copy()

        aug_idxes = self._get_random_aug_idxes(tokens)
        aug_idxes.sort(reverse=True)

        for aug_idx in aug_idxes:
            results.insert(aug_idx, nml.BertDeprecated.MASK)
            predict_results = self.model.predict(results, nml.BertDeprecated.MASK, self.aug_n)
            # Temp fix or sampling issue
            if len(predict_results) > 0:
                new_word = self.sample(predict_results, 1)[0]
                results[aug_idx] = new_word

        return self.reverse_tokenizer(results)

    def substitute(self, data):
        tokens = self.tokenizer(data)
        results = tokens.copy()

        aug_idxes = self._get_aug_idxes(tokens)

        for aug_idx in aug_idxes[:1]:
            original_word = results[aug_idx]
            candidate_words = self.model.predict(results, original_word, top_n=self.aug_n)
            substitute_word = self.sample(candidate_words, 1)[0]

            results[aug_idx] = substitute_word

        final_results = []
        for src, dest in zip(tokens, results):
            final_results.append(self.align_capitalization(src, dest))

        return self.reverse_tokenizer(final_results)

    def get_model(self, device='cpu', force_reload=False):
        return init_bert_model_deprecated(self.model_path, device, self.tokenizer_path, force_reload)
