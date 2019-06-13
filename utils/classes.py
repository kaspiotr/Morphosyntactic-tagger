class Paragraph:
    def __init__(self, paragraph_tag):
        self.paragraph_tag = paragraph_tag
        self.sentences = []

    def add_sentence(self, sentence):
        self.sentences.append(sentence)

    def create_paragraph_line_string(self):
        paragraph_str = "{\"sentence\": ["
        for sentence in self.sentences:
            if sentence is not self.sentences[0]:
                paragraph_str += ", "
            paragraph_str += sentence.create_sentence_line_str()
        paragraph_str += "]}"
        return paragraph_str

    def create_paragraph_dict(self):
        paragraph_dict = {"sentence": []}
        for sentence in self.sentences:
            paragraph_dict["sentence"].append(sentence.create_sentence_dict())
        return paragraph_dict


class Sentence:
    def __init__(self, sentence_tag):
        self.sentence_tag = sentence_tag
        self.tokens = []

    def add_token(self, token):
        self.tokens.append(token)

    def create_sentence_line_str(self):
        sentence_str = "{\"token\": ["
        for token in self.tokens:
            if token is not self.tokens[0]:
                sentence_str += ", "
            sentence_str += token.create_token_line_str()
        sentence_str += "]}"
        return sentence_str

    def create_sentence_dict(self):
        sentence_dict = {"token": []}
        for token in self.tokens:
            sentence_dict["token"].append(token.create_token_dict())
        return sentence_dict


class Token:
    def __init__(self, token_tag):
        self.token_tag = token_tag
        self.changed_form = None
        self.base_form = None
        self.tag = None
        self.separator = False
        self.proposed_tags = []

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
        token_str += "\"changed_form\": \""
        token_str += "\\\"" if len(self.changed_form) == 1 and ord(self.changed_form) == 34 else self.changed_form
        token_str += "\", "
        token_str += "\"base_form\": \""
        token_str += "\\\"" if len(self.base_form) == 1 and ord(self.base_form) == 34 else self.base_form
        token_str += "\", "
        token_str += "\"tag\": \""
        token_str += self.tag
        token_str += "\", "
        token_str += "\"separator\": "
        token_str += "true" if self.separator else "false"
        token_str += ", "
        token_str += "\"proposed_tags\": ["
        for index in range(0, len(self.proposed_tags)):
            if index != 0:
                token_str += ", "
            if self.proposed_tags[index] is None:
                continue
            token_str += "{\"tag\": \""
            token_str += "\\\"" if len(str(self.proposed_tags[index])) == 1 and ord(str(self.proposed_tags[index])) == 34 else str(self.proposed_tags[index].split(":")[0])
            token_str += "\","
            token_str += "\"changed_form\": \""
            token_str += str(":".join(self.proposed_tags[index].split(":")[1:]))
            token_str += "\"}"
        token_str += "]}"
        return token_str

    def create_token_dict(self):
        token_dict = {}
        token_dict["changed_form"] = self.changed_form
        token_dict["base_form"] = self.base_form
        token_dict["tag"] = self.tag
        token_dict["separator"] = self.separator
        token_dict["proposed_tags"] = []
        for base_form_with_tag in self.proposed_tags:
            if base_form_with_tag is None:
                continue
            base_form = base_form_with_tag.split(":")[0]
            tag = ":".join(base_form_with_tag.split(":")[1:])
            proposed_tag = {}
            proposed_tag["base_form"] = base_form
            proposed_tag["tag"] = tag
            token_dict["proposed_tags"].append(proposed_tag)
        return token_dict
