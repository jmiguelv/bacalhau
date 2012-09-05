from nltk.corpus import wordnet
import re


class Text(object):
    """Represents a text unit from a `Document`."""

    def __init__(self, text_id, content, tokenizer, stopwords):
        """Creates a new Text object."""
        self._text_id = text_id
        self._content = content.lower()
        self._tokenizer = tokenizer
        self._stopwords = stopwords

    def get_term_data(self):
        """Returns a dictionary of term data for this text.

        Terms are keys, values are dictionaries of frequency counts
        keyed by text id.

        """
        term_data = {}
        tokens = self._tokenizer.tokenize(self._content)
        max_token_count = 0
        # This provides a "term count" that is unnormalised, meaning
        # that the length of the text is not accounted for.
        for token in tokens:
            if self._is_valid_token(token):
                token_data = term_data.setdefault(token,
                        {self._text_id: {'count': 0}})
                if (token_data[self._text_id]['count'] + 1) > max_token_count:
                    max_token_count += 1
                term_data[token][self._text_id]['count'] += 1
        # Normalise the term counts to provide a "term frequency" for
        # each term.
        for term, text_data in term_data.items():
            count = float(text_data[self._text_id]['count'])
            text_data[self._text_id]['frequency'] = count / max_token_count
        return term_data

    def _is_valid_token(self, token):
        """Returns True if `token` is suitable for processing."""
        if token in self._stopwords:
            return False
        if re.search(r'[^A-Za-z]', token):
            return False
        if not wordnet.synsets(token, pos=wordnet.NOUN):
            return False
        return True
