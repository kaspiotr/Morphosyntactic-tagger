class Paragraph:
    def __init__(self, paragraph_tag):
        self.paragraph_tag = paragraph_tag
        self.sentences = []

    def add_sentence(self, sentence):
        self.sentences.append(sentence)

    def create_paragraph_line_string(self):
        paragraph_str = r"{["
        for sentence in self.sentences:
            paragraph_str += sentence.create_sentence_line_str()
        paragraph_str += "]}"
        return paragraph_str

    def __iter__(self):
        return self.sentences.__iter__()


class Sentence:
    def __init__(self, sentence_tag):
        self.sentence_tag = sentence_tag
        self.tokens = []

    def add_token(self, token):
        self.tokens.append(token)

    def create_sentence_line_str(self):
        sentence_str = "{["
        for token in self.tokens:
            sentence_str += token.create_token_line_str()
        sentence_str += "]}"
        return sentence_str

    def text(self):
        return ''.join(map(lambda token: ' '+token.form if token.space_before else token.form, self.tokens))

    def __iter__(self):
        return self.tokens.__iter__()


class Token:
    def __init__(self, token_tag):
        self.token_tag = token_tag
        self.changed_form = None
        self.base_form = None
        self.tag = None
        self.separator = False
        self.proposed_tags = []
        self.space_before = None
        self.interpretations = []
        self.gold_form = None

    def add_changed_form(self, changed_form):
        self.changed_form = changed_form

    def add_base_form(self, base_form):
        self.base_form = base_form

    def add_tag(self, tag):
        self.tag = tag

    def add_separator(self, separator):
        self.separator = separator

    def add_proposed_tags(self, proposed_tag):
        self.proposed_tags.append(proposed_tag)

    def create_token_line_str(self):
        token_str = "{"
        token_str += "\"changed_form\":\""
        token_str += self.changed_form
        token_str += "\","
        token_str += "\"base_form\":\""
        token_str += self.base_form
        token_str += "\","
        token_str += "\"tag\":\""
        token_str += self.tag
        token_str += "\","
        token_str += "\"separator\":\""
        token_str += str(self.separator)
        token_str += "\","
        token_str += "\"proposed_tags\":["
        for tag in self.proposed_tags:
            if tag is not self.proposed_tags[0]:
                token_str += ","
            token_str += "\""
            token_str += tag
            token_str += "\""
        token_str += "]}"
        return token_str

    def add_interpretation(self, interpretation):
        self.interpretations.append(interpretation)

    def __str__(self):
        return 'Token(%s, %s)' % (self.form, self.interpretations)




