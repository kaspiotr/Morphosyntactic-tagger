import argparse
import csv
import jsonlines
import numpy as np
import os
import glob
import sys
import xml.etree.ElementTree as ET
from convert_tsv_to_xml import prettify
from sklearn.model_selection import StratifiedKFold
from training import map_paragraph_id_to_text_category_name, write_to_file
from utils.nkjp_corpora_utils import correct_nkjp_base_form_and_tag_format


def _print_proposed_tags(proposed_tags_list):
    if not proposed_tags_list:
        return ' proposed_tags:'
    proposed_tags_string = ""
    for idx, proposed_tag in enumerate(proposed_tags_list):
        proposed_tags_delimiter = ' proposed_tags:' if idx == 0 else '#|#'
        proposed_tags_string += proposed_tags_delimiter + proposed_tag['base_form'] + '#=#' + proposed_tag['tag']
    return proposed_tags_string


def _write_paragraph_to_file(paragraphs_np_array, paragraphs_indexes, destination_file_name):
    for paragraph_json_idx in paragraphs_indexes:
        for sentence in paragraphs_np_array.item(paragraph_json_idx)["sentences"]:
            for token in sentence["sentence"]:
                token_json = token["token"]
                write_to_file(destination_file_name, token_json["changed_form"] + " " + token_json["base_form"].strip()
                              + " " + token_json["tag"] + " " + str(token_json["separator"])
                              + _print_proposed_tags(token_json["proposed_tags"]) + "\n")
            write_to_file(destination_file_name, "\n")


def convert_nkjp_base_form_and_tag_to_ref_files(nkjp_output_file_path):
    if '/'.join(nkjp_output_file_path.split('/')[:-1]) == '/resources':
        file_name = nkjp_output_file_path.split('/')[-1]
        nkjp_output_file = os.path.dirname(os.path.abspath(__file__)) + '/resources/' + file_name + '.jsonl'
    else:
        nkjp_output_file = nkjp_output_file_path
    data_folder = os.path.dirname(os.path.abspath(__file__)) + '/nkjp_data'
    with jsonlines.open(nkjp_output_file) as reader:
        skf = StratifiedKFold(n_splits=10, shuffle=False, random_state=None)
        text_category_to_number_of_elements = {}
        paragraphs_X = []
        paragraph_text_category_y = []
        for paragraph in reader:
            paragraphs_X.append(paragraph)
            paragraph_text_category_y.append(map_paragraph_id_to_text_category_name(paragraph, text_category_to_number_of_elements))
        X = np.array(paragraphs_X)
        y = np.array(paragraph_text_category_y)
        skf_split_no = 1
        for _, test_index in skf.split(X, y):
            test_file_name = data_folder + "/nkjp_ref_" + str(skf_split_no)
            _write_paragraph_to_file(X, test_index, test_file_name)
            skf_split_no += 1


def read_sentence_from_tsv(skf_split_no):
    with open("nkjp_data/nkjp_ref_" + skf_split_no) as fd:
        rd = csv.reader(fd, delimiter="\t")
        sentence = []
        for row in rd:
            if row:
                concatenated_sentences_list = row[0].split("\n\n")
                first_from_concatenated_sentences = True
                for sentence_string in concatenated_sentences_list:
                    concatenated_rows_list = sentence_string.split("\n")
                    for single_row in concatenated_rows_list:
                        sentence.append(single_row)
                    if not first_from_concatenated_sentences:
                        if sentence[0] != '':
                            yield sentence
                        sentence.clear()
                    first_from_concatenated_sentences = False
            else:
                yield sentence
                sentence.clear()


def _create_orth_and_lex_objects(token_data, token_object):
    orth = ET.SubElement(token_object, 'orth')
    lex = ET.SubElement(token_object, 'lex', disamb='1')
    base = ET.SubElement(lex, 'base')
    ctag = ET.SubElement(lex, 'ctag')
    base_form_with_tag = token_data[0:token_data.find(' proposed_tags:')]
    proposed_tags = token_data[token_data.find(' proposed_tags:') + 15:]
    base_form, tag = correct_nkjp_base_form_and_tag_format(' '.join(base_form_with_tag.split(' ')[1:-2]) + ":" + base_form_with_tag.split(' ')[-2])
    orth.text = token_data.split(' ')[0]
    base.text = base_form
    ctag.text = tag
    if proposed_tags != '':
        for proposed_tag in proposed_tags.split(' ')[-1].split('#|#'):
            if proposed_tag != '' and proposed_tag.find('num') == -1:
                if proposed_tag.split('#=#')[1] == 'ign':
                    proposed_tag_lex = ET.SubElement(token_object, 'lex')
                    proposed_tag_base = ET.SubElement(proposed_tag_lex, 'base')
                    prepared_proposed_tag_tag = 'None' if proposed_tag.split('#=#')[0] == '' else proposed_tag.split('#=#')[0]
                    proposed_tag_base_form, proposed_tag_tag = correct_nkjp_base_form_and_tag_format(prepared_proposed_tag_tag + ":" + proposed_tag.split('#=#')[1])
                    proposed_tag_base.text = proposed_tag_base_form
                    proposed_tag_ctag = ET.SubElement(proposed_tag_lex, 'ctag')
                    proposed_tag_ctag.text = proposed_tag_tag


def _create_token_object(sentence_data, sentence_object):
    for token_data in sentence_data:
        if token_data.split(' ')[3] == 'False':
            ET.SubElement(sentence_object, 'ns')
        token = ET.SubElement(sentence_object, 'tok')
        _create_orth_and_lex_objects(token_data, token)


def create_xml_file(paragraph_object, skf_split_no):
    for sentence_data in read_sentence_from_tsv(skf_split_no):
        sentence_object = ET.SubElement(paragraph_object, 'chunk', type='s')
        _create_token_object(sentence_data, sentence_object)


def convert_nkjp_ref_to_xml(nkjp_ref_file_path):
    split_no = nkjp_ref_file_path.split("/")[-1].split("_")[-1]
    csv.field_size_limit(sys.maxsize)
    xml_doc = ET.Element('cesAna', version="1.0", type="lex disamb")
    xml_doc.set("xmlns:xlink", "http://www.w3.org/1999/xlink")
    chunk_list = ET.SubElement(xml_doc, 'chunkList')
    paragraph = ET.SubElement(chunk_list, 'chunk', type='p')
    create_xml_file(paragraph, split_no)
    prettify(xml_doc)
    tree = ET.ElementTree(xml_doc)
    root = tree.getroot()
    with open("resources/nkjp_ref_" + split_no + ".xml", "w", encoding='UTF-8') as xf:
        doc_type = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE cesAna ' \
               'SYSTEM "xcesAnaIPI.dtd">\n'
        to_string = ET.tostring(root, encoding='utf-8').decode('utf-8')
        file = f"{doc_type}{to_string}"
        xf.write(file)


def convert_nkjp_to_xml():
    path = os.path.abspath(os.path.dirname(os.path.abspath(__file__))) + "/nkjp_data/*"
    nkjp_ref_files = glob.iglob(path)
    for nkjp_ref_file_path in nkjp_ref_files:
        convert_nkjp_ref_to_xml(nkjp_ref_file_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-file_path",
                        help="The absolute path with name of the saved *.jsonl file or just the name of that file.",
                        default='/resources/nkjp_output',
                        type=str)
    args = parser.parse_args()
    convert_nkjp_base_form_and_tag_to_ref_files(args.file_path)
    convert_nkjp_to_xml()


if __name__ == '__main__':
    main()
