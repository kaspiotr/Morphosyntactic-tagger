import gensim
from flair import file_utils
from pathlib import Path
from training import use_scratch_dir_if_available
import os


def download_and_save_embeddings_model(save_path):
    if not os.path.exists(save_path):
        cache_dir = Path('embeddings')
        file_path = file_utils.cached_path(
            f"https://flair.informatik.hu-berlin.de/resources/embeddings/token/pl-wiki-fasttext-300d-1M",
            cache_dir=cache_dir)
        polish_word_embeddings = gensim.models.KeyedVectors.load(str(file_path))
        polish_word_embeddings.save(save_path)


def main():
    download_and_save_embeddings_model(use_scratch_dir_if_available('resources/polish_FastText_embeddings'))


if __name__ == '__main__':
    main()
