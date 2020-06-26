import csv
import os
import glob
import sys
import re
import xml.etree.ElementTree as ET


def prettify(element, indent=' '):
    queue = [(0, element)]  # (level, element)
    while queue:
        level, element = queue.pop(0)
        children = [(level + 1, child) for child in list(element)]
        if children and len(children) == 2 and children[0][1].tag == 'base' and children[1][1].tag == 'ctag':
            element.tail = '\n' + indent * (level - 1)  # for parent close
        else:
            if children:
                if children[0][1].tag != 'cesAna':
                    element.text = '\n' + indent * level  # for child open
                else:
                    element.text = '\n' + indent * (level + 1)  # for child open
            if queue:
                if element.tag != 'orth':
                    if element.tag == 'tok' or element.tag == 'ns' or element.tag == 'chunk':
                        element.tail = '\n' + indent * (queue[0][0] - 1)
                    else:
                        element.tail = '\n' + indent * queue[0][0]  # for sibling open
                else:
                    element.tail = '\n' + indent * (queue[0][0] - 1)
                    value = queue.pop(0)
                    queue.insert(0, [value[0] - 1, value[1]])
            else:
                if element.tag != 'chunkList':
                    element.tail = '\n' + indent * (level - 1)  # for parent close
                else:
                    element.tail = '\n' + indent * level
            queue[0:0] = children  # prepend so children come before siblings


def _create_token_object(sentence_data, sentence_object):
    for token_data in sentence_data:
        if token_data.split(' ')[0] == '.':
            ET.SubElement(sentence_object, 'ns')
        token = ET.SubElement(sentence_object, 'tok')
        _create_orth_and_lex_objects(token_data, token)


def _create_orth_and_lex_objects(token_data, token_object):
    orth = ET.SubElement(token_object, 'orth')
    lex = ET.SubElement(token_object, 'lex', disamb='1')
    base = ET.SubElement(lex, 'base')
    ctag = ET.SubElement(lex, 'ctag')
    orth.text = token_data.split(' ')[0]
    base.text = token_data.split(' ')[0]
    ctag.text = re.sub("num:::", "ign", token_data.split(' ')[1])


def convert_tsv_to_xml(tsv_file_path):
    split_no = tsv_file_path.split("/")[-2].split("-")[-1]
    csv.field_size_limit(sys.maxsize)
    xml_doc = ET.Element('cesAna', version="1.0", type="lex disamb")
    xml_doc.set("xmlns:xlink", "http://www.w3.org/1999/xlink")
    chunk_list = ET.SubElement(xml_doc, 'chunkList')
    paragraph = ET.SubElement(chunk_list, 'chunk', type='p')
    create_xml_file(paragraph)
    prettify(xml_doc)
    tree = ET.ElementTree(xml_doc)
    root = tree.getroot()
    with open("resources/test_" + split_no + ".xml", "w", encoding='UTF-8') as xf:
        doc_type = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE cesAna ' \
               'SYSTEM "xcesAnaIPI.dtd">\n'
        to_string = ET.tostring(root, encoding='utf-8').decode('utf-8')
        file = f"{doc_type}{to_string}"
        xf.write(file)


def create_xml_file(paragraph_object):
    for sentence_data in read_sentence_from_tsv():
        sentence_object = ET.SubElement(paragraph_object, 'chunk', type='s')
        _create_token_object(sentence_data, sentence_object)


def read_sentence_from_tsv():
    with open("resources/taggers/example-pos/it-2/test.tsv") as fd:
        rd = csv.reader(fd, delimiter="\t")
        sentence = []
        for row in rd:
            if row:
                sentence.append(row[0])
            else:
                yield sentence
                sentence.clear()


def main():
    path = os.path.abspath(os.path.dirname(os.path.abspath(__file__))) + "/resources/taggers/example-pos/*/test.tsv"
    tsv_files = glob.iglob(path)
    for tsv_file_path in tsv_files:
        convert_tsv_to_xml(tsv_file_path)


if __name__ == '__main__':
    main()
