from flair.data import Sentence
from flair.models import SequenceTagger


def main():
    # load the model you trained
    model = SequenceTagger.load('resources/taggers/example-pos/best-model.pt')

    # create example sentence
    sentence = Sentence('Placek ziemniaczany są lepsze niż kremówki')

    # predict tags and print
    model.predict(sentence)

    print(sentence.to_tagged_string())


if __name__ == '__main__':
    main()
