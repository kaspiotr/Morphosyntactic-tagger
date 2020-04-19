class Paragraph:
    def __init__(self, paragraph_tag):
        self.paragraph_id = ""
        self.paragraph_tag = paragraph_tag
        self.sentences = []

    def add_sentence(self, sentence):
        self.sentences.append(sentence)

    def create_paragraph_dict(self, paragraph_id):
        self.paragraph_id = paragraph_id
        paragraph_dict = {"id": paragraph_id, "sentences": []}
        sentence_no = 1
        for sentence in self.sentences:
            sentence_id = paragraph_id + '-' + str(sentence_no)
            paragraph_dict["sentences"].append(sentence.create_sentence_dict(sentence_id))
            sentence_no += 1
        return paragraph_dict


class Sentence:
    def __init__(self, sentence_tag):
        self.sentence_id = ""
        self.sentence_tag = sentence_tag
        self.tokens = []

    def add_token(self, token):
        self.tokens.append(token)

    def create_sentence_dict(self, sentence_id):
        self.sentence_id = sentence_id
        sentence_dict = {"sentence": [], "match": False, "id": sentence_id}
        token_no = 1
        for token in self.tokens:
            token_id = sentence_id + '-' + str(token_no)
            sentence_dict["sentence"].append(token.create_token_dict(token_id))
            token_no += 1
        return sentence_dict


class Token:
    def __init__(self, token_tag):
        self.token_id = ""
        self.token_tag = token_tag
        self.changed_form = None
        self.base_form = None
        self.tag = None
        self.separator = True
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

    def create_token_dict(self, token_id):
        token_dict = {"token": {"changed_form": self.changed_form, "base_form": self.base_form, "tag": self.tag,
                      "separator": self.separator, "proposed_tags": [], "id": token_id}}
        for base_form_with_tag in self.proposed_tags:
            if base_form_with_tag is None:
                continue
            base_form = base_form_with_tag.split(":")[0]
            tag = ":".join(base_form_with_tag.split(":")[1:])
            proposed_tag = {}
            proposed_tag["base_form"] = base_form
            proposed_tag["tag"] = tag
            token_dict["token"]["proposed_tags"].append(proposed_tag)
        return token_dict
