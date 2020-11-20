from flair.data import Corpus
from flair.datasets import ColumnCorpus
from flair.embeddings import FlairEmbeddings, StackedEmbeddings, TokenEmbeddings, OneHotEmbeddings, WordEmbeddings
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer
from flair.visual.training_curves import Plotter
from training import use_scratch_dir_if_available, prepare_skf_splits_data_folder, \
    prepare_resources_pol_eval_file_path, write_to_file
from typing import List
import argparse
import os
import xml.etree.ElementTree as ET
import logging as log
import math
import flair
import torch
import sys


def train_sequence_labeling_model(data_folder, proposed_tags_vocabulary_size):
    # define columns
    columns = {0: 'text', 1: 'pos', 2: 'is_separator', 3: 'proposed_tags'}
    # init a corpus using column format, data folder and the names of the train and test files
    # 1. get the corpus
    corpus: Corpus = ColumnCorpus(data_folder, columns,
                                  train_file='train',
                                  test_file='test',
                                  dev_file=None)
    log.info(corpus)
    # 2. what tag do we want to predict
    tag_type = 'pos'
    # 3. make the tag dictionary from the corpus
    tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)
    log.info(tag_dictionary)
    # 4. initialize embeddings
    local_model_path = use_scratch_dir_if_available('resources/polish_FastText_embeddings')
    embedding_types: List[TokenEmbeddings] = [
        FlairEmbeddings('pl-forward', chars_per_chunk=64),
        FlairEmbeddings('pl-backward', chars_per_chunk=64),
        OneHotEmbeddings(corpus=corpus, field='is_separator', embedding_length=3, min_freq=3),
        OneHotEmbeddings(corpus=corpus, field='proposed_tags',
                         embedding_length=math.ceil((proposed_tags_vocabulary_size + 1)**0.25),
                         min_freq=3),
        WordEmbeddings(local_model_path) if os.path.exists(local_model_path) else WordEmbeddings('pl')
    ]
    embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)
    # 5. initialize sequence tagger
    tagger: SequenceTagger = SequenceTagger(hidden_size=256,
                                            embeddings=embeddings,
                                            tag_dictionary=tag_dictionary,
                                            tag_type=tag_type,
                                            use_crf=False,
                                            rnn_layers=2)
    # 6. initialize trainer
    trainer: ModelTrainer = ModelTrainer(tagger, corpus)
    # 7. start training
    trainer.train(use_scratch_dir_if_available('resources_pol_eval/taggers/example-pos/'),
                  learning_rate=0.1,
                  mini_batch_size=32,
                  embeddings_storage_mode='gpu',
                  max_epochs=sys.maxsize,
                  monitor_test=True)
    # 8. plot weight traces (optional)
    plotter = Plotter()
    plotter.plot_weights(use_scratch_dir_if_available('resources_pol_eval/taggers/example-pos/weights.txt'))


def train(train_gold_file_path, train_analyzed_file_path):
    log.basicConfig(filename=use_scratch_dir_if_available('resources_pol_eval/training.log'),
                    format='%(levelname)s:%(message)s', level=log.INFO)
    log.info(flair.device)
    log.info("Is CUDA available: %s " % torch.cuda.is_available())
    if '/'.join(train_gold_file_path.split('/')[:-1]) == '/resources_pol_eval':
        file_name = train_gold_file_path.split('/')[-1]
        train_gold_file = prepare_resources_pol_eval_file_path(file_name)
    else:
        train_gold_file = train_gold_file_path
    if '/'.join(train_analyzed_file_path.split('/')[:-1]) == '/resources_pol_eval':
        file_name = train_analyzed_file_path.split('/')[-1]
        train_analyzed_file = prepare_resources_pol_eval_file_path(file_name)
    else:
        train_analyzed_file = train_analyzed_file_path
    # this is the folder in which train and test files reside
    data_folder = prepare_skf_splits_data_folder('data_pol_eval')
    train_file_name = data_folder + "/train"
    test_file_name = data_folder + "/test"
    create_train_data_file_from_xml(parse_xml, train_gold_file, train_analyzed_file, train_file_name)
    proposed_tags_dict = {}
    # for paragraph in reader:
    #         paragraphs_X.append(paragraph)
    #         paragraph_text_category_y.append(map_paragraph_id_to_text_category_name(paragraph, text_category_to_number_of_elements))
    #             _write_paragraph_to_file(X, train_index, train_file_name, proposed_tags_dict, False)
    #             _write_paragraph_to_file(X, test_index, test_file_name, proposed_tags_dict)
    #             total_proposed_tags_no = 0
    #             for tag in proposed_tags_dict:
    #                 total_proposed_tags_no += proposed_tags_dict[tag]
    #             log.info("Total proposed tags no.: %s" % total_proposed_tags_no)
    #             log.info("Proposed tags classes no.: %s" % len(proposed_tags_dict))
    #             train_sequence_labeling_model(data_folder, len(proposed_tags_dict))
    #         iteration_no += 1


def parse_proposed_tags_from_train_analyzed_file(train_analyzed_file_path, line_content, generator):
    is_first_proposed_tag = True
    for event_analyzed_file, element_analyzed_file in generator:
        if event_analyzed_file == "start":
            if element_analyzed_file.tag == "ctag":
                if not is_first_proposed_tag:
                    line_content += ";"
                else:
                    is_first_proposed_tag = False
        if event_analyzed_file == "end":
            if element_analyzed_file.tag == "ctag":
                line_content += element_analyzed_file.text
            if element_analyzed_file.tag == "tok":
                is_first_proposed_tag = True
                line_content += "\n"
                yield line_content, generator


def parse_xml(train_gold_file_path, train_analyzed_file_path):
    line_content = ""
    is_first_sentence_of_file = True
    is_first_token_in_sentence = True
    ns_occurred = False
    generator = ET.iterparse(train_analyzed_file_path, events=("start", "end",))
    for event, element in ET.iterparse(train_gold_file_path, events=("start", "end",)):
        if event == "start":
            if element.tag == 'ns':
                ns_occurred = True
            if element.tag == 'tok':
                if not is_first_token_in_sentence:
                    line_content += "\n"
                else:
                    is_first_sentence_of_file = False
            if element.tag == 'chunk' and element.get('type') == 's':
                is_first_token_in_sentence = True
        if event == "end":
            if element.tag == "orth":
                line_content += element.text
            if element.tag == "ctag":
                line_content += " " + element.text
            if element.tag == "tok":
                if ns_occurred:
                    line_content += " False "
                    ns_occurred = False
                else:
                    line_content += " True "
                line_content, generator = next(parse_proposed_tags_from_train_analyzed_file(train_analyzed_file_path, line_content, generator))
                yield line_content
                element.clear()
                line_content = ""
            if element.tag == 'chunk' and element.get('type') == 's':
                if not is_first_sentence_of_file:
                    line_content += "\n"
                else:
                    is_first_sentence_of_file = False


def create_train_data_file_from_xml(parsing_generator, train_gold_file_path, train_analyzed_file_path, train_file_path):
    for train_file_line in parsing_generator(train_gold_file_path, train_analyzed_file_path):
        write_to_file(train_file_path, train_file_line)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-train_gold_file_path",
                        help="The absolute path with name of the saved train-gold.xml file or just the name of that file.",
                        default=use_scratch_dir_if_available('/resources_pol_eval/train-gold'),
                        type=str)
    parser.add_argument("-train_analyzed_file_path",
                        help="The absolute path with name of the saved train-analyzed.xml file or just the name of that file.",
                        default=use_scratch_dir_if_available('/resources_pol_eval/train-analyzed'),
                        type=str)
    args = parser.parse_args()
    train(args.train_gold_file_path, args.train_analyzed_file_path)


if __name__ == '__main__':
    main()
