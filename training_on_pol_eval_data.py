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


def train(train_gold_file_path, train_analyzed_file_path, test_analyzed_file_path, gold_task_a_b_file_path):
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
    if '/'.join(gold_task_a_b_file_path.split('/')[:-1]) == '/resources_pol_eval':
        file_name = gold_task_a_b_file_path.split('/')[-1]
        gold_task_a_b_file = prepare_resources_pol_eval_file_path(file_name)
    else:
        gold_task_a_b_file = gold_task_a_b_file_path
    if '/'.join(test_analyzed_file_path.split('/')[:-1]) == '/resources_pol_eval':
        file_name = test_analyzed_file_path.split('/')[-1]
        test_analyzed_file_path = prepare_resources_pol_eval_file_path(file_name)
    else:
        test_analyzed_file_path = test_analyzed_file_path
    # this is the folder in which train and test files reside
    data_folder = prepare_skf_splits_data_folder('data_pol_eval')
    train_file_name = data_folder + "/train"
    test_file_name = data_folder + "/test"
    proposed_tags_dict = {}
    create_train_data_file_from_xmls(parse_train_xmls, train_gold_file, train_analyzed_file, train_file_name, proposed_tags_dict)
    create_test_data_file_from_xml(parse_test_xmls, test_analyzed_file_path, gold_task_a_b_file, test_file_name, proposed_tags_dict)
    total_proposed_tags_no = 0
    for tag in proposed_tags_dict:
        total_proposed_tags_no += proposed_tags_dict[tag]
    log.info("Total proposed tags no.: %s" % total_proposed_tags_no)
    log.info("Proposed tags classes no.: %s" % len(proposed_tags_dict))
    train_sequence_labeling_model(data_folder, len(proposed_tags_dict))


def parse_proposed_tags_from_train_analyzed_file(line_content, generator, proposed_tags_dict):
    proposed_tags_list = []
    for event_analyzed_file, element_analyzed_file in generator:
        if event_analyzed_file == "end":
            if element_analyzed_file.tag == "ctag":
                proposed_tags_list.append(element_analyzed_file.text)
            if element_analyzed_file.tag == "tok":
                unique_proposed_tags_list = list(set(proposed_tags_list))
                unique_proposed_tags_list.sort(reverse=False)
                joined_proposed_tag = ";".join(unique_proposed_tags_list)
                if joined_proposed_tag not in proposed_tags_dict:
                    proposed_tags_dict[joined_proposed_tag] = 1
                else:
                    proposed_tags_dict[joined_proposed_tag] += 1
                line_content += joined_proposed_tag
                line_content += "\n"
                yield line_content, generator
                proposed_tags_list = []


def parse_reference_tag_from_gold_task_a_b_file(line_content, generator):
    for event_gold_task_a_b_file, element_gold_task_a_b_file in generator:
        if event_gold_task_a_b_file == "end":
            if element_gold_task_a_b_file.tag == "lex" and element_gold_task_a_b_file.get('disamb') is not None \
                    and element_gold_task_a_b_file.get('disamb') == '1':
                line_content += " " + element_gold_task_a_b_file[1].text
                yield line_content, generator


def parse_test_xmls(test_analyzed_file_path, gold_task_a_b_file_path, proposed_tags_dict):
    line_content = ""
    is_first_sentence_of_file = True
    is_first_token_in_sentence = True
    ns_occurred = False
    proposed_tags = []
    generator = ET.iterparse(gold_task_a_b_file_path, events=("start", "end",))
    for event, element in ET.iterparse(test_analyzed_file_path, events=("start", "end",)):
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
                proposed_tags.append(element.text)
            if element.tag == "tok":
                unique_proposed_tags_list = list(set(proposed_tags))
                unique_proposed_tags_list.sort(reverse=False)
                joined_proposed_tag = ";".join(unique_proposed_tags_list)
                line_content, generator = next(parse_reference_tag_from_gold_task_a_b_file(line_content, generator))
                if ns_occurred:
                    line_content += " False "
                    ns_occurred = False
                else:
                    line_content += " True "
                if joined_proposed_tag not in proposed_tags_dict:
                    proposed_tags_dict[joined_proposed_tag] = 1
                else:
                    proposed_tags_dict[joined_proposed_tag] += 1
                line_content += joined_proposed_tag
                line_content += "\n"
                yield line_content
                proposed_tags = []
                element.clear()
                line_content = ""
            if element.tag == 'chunk' and element.get('type') == 's':
                if not is_first_sentence_of_file:
                    line_content += "\n"
                else:
                    is_first_sentence_of_file = False
    log.info("Length of proposed tags dictionary based on train and test files: %s" % len(proposed_tags_dict))


def parse_train_xmls(train_gold_file_path, train_analyzed_file_path, proposed_tags_dict):
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
                line_content, generator = next(parse_proposed_tags_from_train_analyzed_file(line_content, generator, proposed_tags_dict))
                yield line_content
                element.clear()
                line_content = ""
            if element.tag == 'chunk' and element.get('type') == 's':
                if not is_first_sentence_of_file:
                    line_content += "\n"
                else:
                    is_first_sentence_of_file = False
    log.info("Length of proposed tags dictionary based on train file only: %s" % len(proposed_tags_dict))


def create_train_data_file_from_xmls(parsing_generator, train_gold_file_path, train_analyzed_file_path, train_file_path, proposed_tags_dict):
    for train_file_line in parsing_generator(train_gold_file_path, train_analyzed_file_path, proposed_tags_dict):
        write_to_file(train_file_path, train_file_line)


def create_test_data_file_from_xml(parsing_generator, test_analyzed_file_path, gold_task_a_b_file_path, test_file_path, proposed_tags_dict):
    for test_file_line in parsing_generator(test_analyzed_file_path, gold_task_a_b_file_path, proposed_tags_dict):
        write_to_file(test_file_path, test_file_line)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-train_gold_file_path",
                        help="The absolute path with name of the saved train-gold.xml file or just the name of that"
                             " file.",
                        default=use_scratch_dir_if_available('/resources_pol_eval/train-gold'),
                        type=str)
    parser.add_argument("-train_analyzed_file_path",
                        help="The absolute path with name of the saved train-analyzed.xml file or just the name of that"
                             " file.",
                        default=use_scratch_dir_if_available('/resources_pol_eval/train-analyzed'),
                        type=str)
    parser.add_argument("-test_analyzed_file_path",
                        help="The absolute path with name of the saved test-analyzed.xml file or just the name of that"
                             " file.",
                        default=use_scratch_dir_if_available('/resources_pol_eval/test-analyzed'),
                        type=str)
    parser.add_argument("-gold_task_a_b_file_path",
                        help="The absolute path with name of the saved gold-task-a-b.xml file or just the name of that"
                             " file.",
                        default=use_scratch_dir_if_available('/resources_pol_eval/gold-task-a-b'),
                        type=str)
    args = parser.parse_args()
    train(args.train_gold_file_path, args.train_analyzed_file_path,  args.test_analyzed_file_path,
          args.gold_task_a_b_file_path)


if __name__ == '__main__':
    main()
