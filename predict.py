from flair.data import Sentence
from flair.models import SequenceTagger


def main():
    # load the model you trained
    model = SequenceTagger.load('resources/taggers/example-pos/it-3/best-model.pt')

    # create example sentences
    sentence = Sentence('Mam próbkę analizy morfologicznej .')
    sentence_2 = Sentence('Zjadłem 7 kanapek .')
    sentence_3 = Sentence('" 1 . Ewakuację wojsk niemieckich ze wszystkich terytoriów okupowanych; 2 . Rozwiązanie '
                          'partii nazistowskiej i rozpisanie wolnych wyborów; 3 . Położenie kresu dyktaturze; 4 . '
                          'Przywrócenie dawnej niemieckiej granicy wschodniej sprzed wojny; 5 . Masową redukcję '
                          'potencjału wojskowego, aby zapobiec na przyszłość nowej agresji; 6 . Kontrolę zbrojeń; '
                          '7 . Postawienie pod sąd przywódców nazistowskich i zbrodniarzy wojennych " .')

    # predict tags and print
    model.predict(sentence)
    model.predict(sentence_2)
    model.predict(sentence_3)

    print(sentence.to_tagged_string())
    print(sentence_2.to_tagged_string())
    print(sentence_3.to_tagged_string())


if __name__ == '__main__':
    main()
