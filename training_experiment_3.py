from flair.data import Corpus
from flair.datasets import ColumnCorpus
from flair.embeddings import StackedEmbeddings, TokenEmbeddings, CharacterEmbeddings, WordEmbeddings, OneHotEmbeddings
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer
from flair.visual.training_curves import Plotter
from sklearn.model_selection import StratifiedKFold
from training import map_paragraph_id_to_text_category_name, _write_paragraph_to_file
from typing import List
import argparse
import os
import jsonlines
import logging as log
import math
import numpy as np
import flair
import torch
import sys


def train_sequence_labeling_model(data_folder, proposed_tags_vocabulary_size, skf_split_no):
    """
    Trains the sequence labeling model (by default model uses one RNN layer).
    Model is trained to predict part of speech tag and takes into account information about:
    - text (plain text made of tokens that together form a sentence),
    - occurrence of separator before token,
    - proposed tags for given token.
    It is trained with use of Stacked Embeddings used to combine different embeddings together. Words are embedded
    using a concatenation of three vector embeddings:
    - WordEmbeddings - classic word embeddings. That kind of embeddings are static and word-level, meaning that each
      distinct word gets exactly one pre-computed embedding. Here FastText embeddings trained over polish Wikipedia are
      used.
    - CharacterEmbeddings - allow to add character-level word embeddings during model training. These embeddings are
      randomly initialized when the class is being initialized, so they are not meaningful unless they are trained on
      a specific downstream task. For instance, the standard sequence labeling architecture used by Lample et al. (2016)
      is a combination of classic word embeddings with task-trained character features. Normally this would require to
      implement a hierarchical embedding architecture in which character-level embeddings for each word are computed
      using an RNN and then concatenated with word embeddings. In Flair, this is simplified by treating
      CharacterEmbeddings just like any other embedding class. To reproduce the Lample architecture, there is only
      a need to combine them with standard WordEmbeddings in an embedding stack.
    - One Hot Embeddings - embeddings that encode each word in a vocabulary as a one-hot vector, followed by an
      embedding layer. These embeddings thus do not encode any prior knowledge as do most other embeddings. They also
      differ in that they require to see a Corpus during instantiation, so they can build up a vocabulary consisting of
      the most common words seen in the corpus, plus an UNK token for all rare words.
      There are one One Hot Embeddings used in training: to embed information about proposed tags (concatenated
      with a ';') and appearance of separator before each token.
    Model training is based on stratified 10 fold cross validation split indicated by skf_split_no argument.
    Model and training logs are saved in resources_ex_3/taggers/example-pos/it-<skf_split_no> directory (where
    <skf_split_no> is the number of stratified 10 fold cross validation split used to train the model).

    :param data_folder: folder where files with column corpus split are stored. Those columns are used to initialize
    ColumnCorpus object
    :param proposed_tags_vocabulary_size: number of proposed tags
    :param skf_split_no: number that indicates one of stratified 10 fold cross validation splits (from range 1 to 10)
    used to train the model
    """
    # define columns
    columns = {0: 'text', 1: 'pos', 2: 'is_separator', 3: 'proposed_tags'}
    # init a corpus using column format, data folder and the names of the train and test files
    # 1. get the corpus
    corpus: Corpus = ColumnCorpus(data_folder, columns,
                                  train_file='train_' + str(skf_split_no),
                                  test_file='test_' + str(skf_split_no),
                                  dev_file=None)
    log.info(corpus)
    # 2. what tag do we want to predict
    tag_type = 'pos'
    # 3. make the tag dictionary from the corpus
    tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)
    log.info(tag_dictionary)
    # 4. initialize embeddings
    local_model_path = 'resources/polish_FastText_embeddings'
    embedding_types: List[TokenEmbeddings] = [
        WordEmbeddings(local_model_path) if os.path.exists(local_model_path) else WordEmbeddings('pl'),
        CharacterEmbeddings(),
        OneHotEmbeddings(corpus=corpus, field='is_separator', embedding_length=3, min_freq=3),
        OneHotEmbeddings(corpus=corpus, field='proposed_tags',
                         embedding_length=math.ceil((proposed_tags_vocabulary_size + 1) ** 0.25),
                         min_freq=3)
    ]
    embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)
    # 5. initialize sequence tagger
    tagger: SequenceTagger = SequenceTagger(hidden_size=256,
                                            embeddings=embeddings,
                                            tag_dictionary=tag_dictionary,
                                            tag_type=tag_type,
                                            use_crf=False,
                                            rnn_layers=1)
    # 6. initialize trainer
    trainer: ModelTrainer = ModelTrainer(tagger, corpus)
    # 7. start training
    trainer.train('resources_ex_3/taggers/example-pos/it-' + str(skf_split_no),
                  learning_rate=0.1,
                  mini_batch_size=32,
                  embeddings_storage_mode='gpu',
                  max_epochs=sys.maxsize,
                  monitor_test=True)
    # 8. plot weight traces (optional)
    plotter = Plotter()
    plotter.plot_weights('resources_ex_3/taggers/example-pos/it-' + str(skf_split_no) + '/weights.txt')


def train(skf_split_no, jsonl_file_path):
    """
    Trains a sequence labeling model using stratified 10-fold cross-validation, which means that model is trained for
    each division of corpora into test and train data (dev data are sampled from train data) (preserving the percentage
    of samples for each class). Each model consists of 1 RNN layer.
    Model is trained to predict part of speech tag and takes into account information about:
    - text (plain text made of tokens that together form a sentence),
    - occurrence of separator before token,
    - proposed tags for given token (taken from MACA analyzer).
    It is trained with use of Stacked Embeddings used to combine different embeddings together. Words are embedded
    using a concatenation of three vector embeddings:
    - WordEmbeddings - classic word embeddings. That kind of embeddings are static and word-level, meaning that each
      distinct word gets exactly one pre-computed embedding. Here FastText embeddings trained over polish Wikipedia are
      used.
    - CharacterEmbeddings - allow to add character-level word embeddings during model training. These embeddings are
      randomly initialized when the class is being initialized, so they are not meaningful unless they are trained on
      a specific downstream task. For instance, the standard sequence labeling architecture used by Lample et al. (2016)
      is a combination of classic word embeddings with task-trained character features. Normally this would require to
      implement a hierarchical embedding architecture in which character-level embeddings for each word are computed
      using an RNN and then concatenated with word embeddings. In Flair, this is simplified by treating
      CharacterEmbeddings just like any other embedding class. To reproduce the Lample architecture, there is only
      a need to combine them with standard WordEmbeddings in an embedding stack.
    - One Hot Embeddings - embeddings that encode each word in a vocabulary as a one-hot vector, followed by an
      embedding layer. These embeddings thus do not encode any prior knowledge as do most other embeddings. They also
      differ in that they require to see a Corpus during instantiation, so they can build up a vocabulary consisting of
      the most common words seen in the corpus, plus an UNK token for all rare words.
      There are one One Hot Embeddings used in training: to embed information about proposed tags (concatenated
      with a ';') and appearance of separator before each token.
    Model training is based on stratified 10 fold cross validation split indicated by skf_split_no argument.
    Model and training logs are saved in resources_ex_3/taggers/example-pos/it-<skf_split_no> directory (where
    <skf_split_no> is the number of stratified 10 fold cross validation split used to train the model).
    Additionally method logs other training log files and saves them in the resources_ex_3 directory of this project
    under the name training_ex_3_<skf_split_no>.log

    :param skf_split_no: stratified 10 fold cross validation split number (from range 1 to 10) used to train the model

    :param jsonl_file_path: file in *.jsonl format with paragraphs in a form of a JSON in each line or absolute path to
    that file
    """
    log.basicConfig(filename='resources_ex_3/training_ex_3_' + str(skf_split_no) + '.log',
                    format='%(levelname)s:%(message)s', level=log.INFO)
    log.info(flair.device)
    log.info("Is CUDA available: %s " % torch.cuda.is_available())
    if '/'.join(jsonl_file_path.split('/')[:-1]) == '/output':
        file_name = jsonl_file_path.split('/')[-1]
        maca_output_serialized_from_nkjp_marked_file = os.path.dirname(os.path.abspath(__file__)) + '/output/' + file_name + '.jsonl'
    else:
        maca_output_serialized_from_nkjp_marked_file = jsonl_file_path
    # this is the folder in which train and test files reside
    data_folder = os.path.dirname(os.path.abspath(__file__)) + '/data_ex_3'
    train_file_name = data_folder + "/train_" + str(skf_split_no)
    test_file_name = data_folder + "/test_" + str(skf_split_no)
    with jsonlines.open(maca_output_serialized_from_nkjp_marked_file) as reader:
        text_category_to_number_of_elements = {}
        paragraphs_X = []
        paragraph_text_category_y = []
        for paragraph in reader:
            paragraphs_X.append(paragraph)
            paragraph_text_category_y.append(map_paragraph_id_to_text_category_name(paragraph, text_category_to_number_of_elements))
        X = np.array(paragraphs_X)
        y = np.array(paragraph_text_category_y)
        skf = StratifiedKFold(n_splits=10, shuffle=False, random_state=None)
        log.info("Number of paragraphs of each text category\n")
        log.info("%-50s%s" % ("Text category", "paragraphs number"))
        for text_cat, els_no in text_category_to_number_of_elements.items():
            log.info("%-50s%s" % (text_cat, els_no))
        proposed_tags_dict = {}
        iteration_no = 1
        for train_index, test_index in skf.split(X, y):
            if iteration_no == skf_split_no:
                log.info("Stratified 10 fold cross validation split number: %d" % iteration_no)
                _write_paragraph_to_file(X, train_index, train_file_name, proposed_tags_dict, False)
                _write_paragraph_to_file(X, test_index, test_file_name, proposed_tags_dict)
                total_proposed_tags_no = 0
                for tag in proposed_tags_dict:
                    total_proposed_tags_no += proposed_tags_dict[tag]
                log.info("Total proposed tags no.: %s" % total_proposed_tags_no)
                log.info("Proposed tags classes no.: %s" % len(proposed_tags_dict))
                train_sequence_labeling_model(data_folder, len(proposed_tags_dict), iteration_no)
            iteration_no += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("skf_split_no", help="The number from range 1 to 10 that indicates the split of stratified "
                                             "10-fold cross validation used to train the model", type=int)
    parser.add_argument("-file_path",
                        help="The absolute path with name of the saved *.jsonl file or just the name of that file.",
                        default='/output/maca_output_marked',
                        type=str)
    args = parser.parse_args()
    train(args.skf_split_no, args.file_path)


if __name__ == '__main__':
    main()
