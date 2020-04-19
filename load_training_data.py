import flair.datasets
from flair.data import Corpus
from flair.datasets import ColumnCorpus


def main():
    corpus = flair.datasets.UD_ENGLISH()
    print(len(corpus.train))
    print(len(corpus.test))
    print(len(corpus.dev))
    print(corpus.test[0])
    print(corpus.test[0].to_tagged_string('pos'))


if __name__ == '__main__':
    main()
