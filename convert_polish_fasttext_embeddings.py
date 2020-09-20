from gensim.models import KeyedVectors
import os


def main():
    word_vectors = KeyedVectors.load(os.path.dirname(os.path.abspath(__file__)) + "/fasttext_v2/fasttext_100_3_polish.bin")
    path_to_converted = os.path.dirname(os.path.abspath(__file__)) + "/fasttext_v2/fasttext_converted"
    word_vectors.save(path_to_converted)


if __name__ == '__main__':
    main()
