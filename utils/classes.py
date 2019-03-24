class Paragraph:
    def __init__(self, paragraph_tag):
        self.paragraph_tag = paragraph_tag
        self.sentences = []

    def add_sentence(self, sentence):
        self.sentences.append(sentence)

    def __iter__(self):
        return self.sentences.__iter__()


class Sentence:
    def __init__(self, sentence_tag):
        self.sentence_tag = sentence_tag
        self.tokens = []

    def add_token(self, token):
        self.tokens.append(token)

    def text(self):
        return ''.join(map(lambda token: ' '+token.form if token.space_before else token.form, self.tokens))

    def __iter__(self):
        return self.tokens.__iter__()


class Token:
    def __init__(self, token_tag):
        self.token_tag = token_tag
        self.changed_form = None
        self.base_form = None
        self.space_before = None
        self.interpretations = []
        self.gold_form = None

    def add_changed_form(self, changed_form):
        self.changed_form = changed_form

    def add_base_form(self, base_form):
        self.base_form = base_form

    def add_interpretation(self, interpretation):
        self.interpretations.append(interpretation)

    def __str__(self):
        return 'Token(%s, %s)' % (self.form, self.interpretations)




