from flair.data import Sentence
from flair.models import SequenceTagger


def main():
    # load the model you trained
    model = SequenceTagger.load('resources/taggers/example-pos/it-3/best-model.pt')

    # create example sentences
    sentence = Sentence('Mam próbkę analizy morfologicznej .')
    sentence_2 = Sentence('Zjadłem 7 kanapek .')

    # predict tags and print
    model.predict(sentence)
    model.predict(sentence_2)

    print(sentence.to_tagged_string())
    print(sentence_2.to_tagged_string())


if __name__ == '__main__':
    main()
