from flair.data import Sentence
from flair.models import SequenceTagger


def main():
    # load the model you trained
    model = SequenceTagger.load('resources/taggers/example-pos/it-3/best-model.pt')

    # create example sentence
    sentence = Sentence('Mam próbkę analizy morfologicznej .')

    # predict tags and print
    model.predict(sentence)

    print(sentence.to_tagged_string())


if __name__ == '__main__':
    main()
