"""
    Augmenter that apply operation (word level) to textual input based on contextual word embeddings.
"""

import string

from nlpaug.augmenter.word import WordAugmenter
import nlpaug.model.lang_models as nml
from nlpaug.util.action import Action

BERT_MODEL = {}
XLNET_MODEL = {}


def init_bert_model(model_path, device, force_reload=False, temperature=1.0, top_k=None, top_p=None):
    # Load model once at runtime

    global BERT_MODEL
    if BERT_MODEL and not force_reload:
        BERT_MODEL.temperature = temperature
        BERT_MODEL.top_k = top_k
        BERT_MODEL.top_p = top_p
        return BERT_MODEL

    bert_model = nml.Bert(model_path, device=device, temperature=temperature, top_k=top_k, top_p=top_p)
    bert_model.model.eval()
    BERT_MODEL = bert_model

    return bert_model


def init_xlnet_model(model_path, device, force_reload=False, temperature=1.0, top_k=None, top_p=None):
    # Load model once at runtime

    global XLNET_MODEL
    if XLNET_MODEL and not force_reload:
        XLNET_MODEL.temperature = temperature
        XLNET_MODEL.top_k = top_k
        XLNET_MODEL.top_p = top_p
        return XLNET_MODEL

    xlnet_model = nml.XlNet(model_path, device=device, temperature=temperature, top_k=top_k, top_p=top_p)
    xlnet_model.model.eval()
    XLNET_MODEL = xlnet_model

    return xlnet_model


class ContextualWordEmbsAug(WordAugmenter):
    """
    Augmenter that leverage contextual word embeddings to find top n similar word for augmentation.

    :param str model_path: Model name or model path. It used transformers to load the model. Tested
        'bert-base-uncased', 'xlnet-base-cased'.
    :param str action: Either 'insert or 'substitute'. If value is 'insert', a new word will be injected to random
        position according to contextual word embeddings calculation. If value is 'substitute', word will be replaced
        according to contextual embeddings calculation
    :param float temperature: Controlling randomness. Default value is 1 and lower temperature results in less random
        behavior
    :param int top_k: Controlling lucky draw pool. Top k score token will be used for augmentation. Larger k, more
        token can be used. Default value is 100. If value is None which means using all possible tokens.
    :param float top_p: Controlling lucky draw pool. Top p of cumulative probability will be removed. Larger p, more
        token can be used. Default value is None which means using all possible tokens.
    :param float aug_p: Percentage of word will be augmented.
    :param int aug_min: Minimum number of word will be augmented.
    :param int aug_max: Maximum number of word will be augmented. If None is passed, number of augmentation is
        calculated via aup_p. If calculated result from aug_p is smaller than aug_max, will use calculated result from
        aug_p. Otherwise, using aug_max.
    :param list stopwords: List of words which will be skipped from augment operation.
    :param bool skip_unknown_word: Do not substitute unknown word (e.g. AAAAAAAAAAA)
    :param str device: Use either cpu or gpu. Default value is None, it uses GPU if having. While possible values are
        'cuda' and 'cpu'.
    :param bool force_reload: Force reload the contextual word embeddings model to memory when initialize the class.
        Default value is False and suggesting to keep it as False if performance is the consideration.
    :param str name: Name of this augmenter

    >>> import nlpaug.augmenter.word as naw
    >>> aug = naw.ContextualWordEmbsAug()
    """

    def __init__(self, model_path='bert-base-uncased', action="substitute", temperature=1.0, top_k=100, top_p=None,
                 name='ContextualWordEmbs_Aug', aug_min=1, aug_max=10, aug_p=0.3, stopwords=None,
                 skip_unknown_word=False, device=None, force_reload=False, verbose=0):
        super().__init__(
            action=action, name=name, aug_p=aug_p, aug_min=aug_min, aug_max=aug_max, tokenizer=None,
            stopwords=stopwords, verbose=verbose)
        self.model_path = model_path
        self.skip_unknown_word = skip_unknown_word
        self.temperature = temperature
        self.top_k = top_k
        self.top_p = top_p

        self._init()
        self.model = self.get_model(
            model_path=model_path, device=device, force_reload=force_reload, temperature=temperature, top_k=top_k,
            top_p=top_p)
        self.device = self.model.device
        self.tokenizer = self.model.tokenizer.tokenize

    def _init(self):
        if 'xlnet' in self.model_path:
            self.model_type = 'xlnet'
        elif 'bert' in self.model_path:
            self.model_type = 'bert'
        else:
            self.model_type = ''

    def skip_aug(self, token_idxes, tokens):
        if not self.skip_unknown_word:
            super().skip_aug(token_idxes, tokens)

        # text is split by " ". Need to join it and tokenizer it by model's tokenizer
        subwords = self.model.tokenizer.tokenize(' '.join(tokens))
        token2subword = {}
        subword_pos = 0

        for i, token in enumerate(tokens):
            token2subword[i] = []

            token2subword[i].append(subword_pos)
            subword_pos += 1

            for subword in subwords[subword_pos:]:
                if self.model_type in ['bert'] and self.model.SUBWORD_PREFIX in subword:
                    token2subword[i].append(subword_pos)
                    subword_pos += 1
                elif self.model_type in ['xlnet'] and self.model.SUBWORD_PREFIX not in subword and \
                        subword not in string.punctuation:
                    token2subword[i].append(subword_pos)
                    subword_pos += 1
                else:
                    break

        results = []
        for token_idx in token_idxes:
            # Skip if includes more than 1 subword. e.g. ESPP --> es ##pp (BERT), ESP --> ESP P (XLNet).
            # Avoid to substitute ESPP token
            if self.action == Action.SUBSTITUTE:
                if len(token2subword[token_idx]) == 1:
                    results.append(token_idx)
            else:
                results.append(token_idx)

        return results

    def split_text(self, data):
        if self.model.model.config.max_position_embeddings == -1:  # e.g. No max length restriction for XLNet
            return data, None

        tokens = self.model.tokenizer.tokenize(data)
        split_pos = self.model.model.config.max_position_embeddings - 2

        # Reverse 2 slot for reserved words (e.g. [CLS] and [SEP] in BERT)
        head_text = self.model.tokenizer.convert_tokens_to_string(tokens[:split_pos]).strip()
        tail_text = None
        if len(tokens) >= split_pos:
            tail_text = self.model.tokenizer.convert_tokens_to_string(tokens[split_pos:]).strip()

        return head_text, tail_text

    def insert(self, data):
        head_text, tail_text = self.split_text(data)
        # Pick target word for augmentation
        tokens = head_text.split(' ')
        aug_idxes = self._get_aug_idxes(tokens)
        if aug_idxes is None or len(aug_idxes) == 0:
            return data
        aug_idxes.sort(reverse=True)

        for aug_idx in aug_idxes:
            tokens.insert(aug_idx, self.model.MASK_TOKEN)
            masked_text = ' '.join(tokens)

            masked_text, local_tail_text = self.split_text(masked_text)
            if local_tail_text is not None:
                tail_text += ' ' + local_tail_text

            candidates = self.model.predict(masked_text, target_word=None, n=1)
            new_word, prob = self.sample(candidates, 1)[0]
            tokens[aug_idx] = new_word

        augmented_text = ' '.join(tokens)
        if tail_text is not None:
            augmented_text += ' ' + tail_text

        return augmented_text

    def substitute(self, data):
        # If length of input is larger than max allowed input, only augment heading part
        head_text, tail_text = self.split_text(data)
        # Pick target word for augmentation
        tokens = head_text.split(' ')
        aug_idxes = self._get_aug_idxes(tokens)
        if aug_idxes is None or len(aug_idxes) == 0:
            return data
        aug_idxes.sort(reverse=True)

        for i, aug_idx in enumerate(aug_idxes):
            original_word = tokens[aug_idx]
            tokens[aug_idx] = self.model.MASK_TOKEN
            masked_text = ' '.join(tokens)

            masked_text, local_tail_text = self.split_text(masked_text)
            if local_tail_text is not None:
                if tail_text is None:
                    tail_text = local_tail_text
                else:
                    tail_text = local_tail_text + ' ' + tail_text

            substitute_word = None
            # https://github.com/makcedward/nlpaug/pull/51
            retry_cnt = 3
            for _ in range(retry_cnt):
                candidates = self.model.predict(masked_text, target_word=original_word, n=1+_)
                if len(candidates) > 0:
                    substitute_word, prob = self.sample(candidates, 1)[0]
                    break

            # TODO: Alternative method better than dropout
            if substitute_word is None:
                substitute_word = ''

            tokens[aug_idx] = substitute_word

        # results = []
        # for src, dest in zip(data.split(' '), tokens):
        #     results.append(self.align_capitalization(src, dest))

        augmented_text = ' '.join(tokens)
        if tail_text is not None:
            augmented_text += ' ' + tail_text

        return augmented_text

    @classmethod
    def get_model(cls, model_path, device='cuda', force_reload=False, temperature=1.0, top_k=None, top_p=0.0):
        if 'bert' in model_path:
            return init_bert_model(model_path, device, force_reload, temperature, top_k, top_p)
        if 'xlnet' in model_path:
            return init_xlnet_model(model_path, device, force_reload, temperature, top_k, top_p)

        raise ValueError('Model name value is unexpected. Only support bert and xlnet model.')
