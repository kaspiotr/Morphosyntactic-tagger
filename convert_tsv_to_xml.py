import csv
import sys
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
                element.text = '\n' + indent * (level + 1)  # for child open
            if queue:
                element.tail = '\n' + indent * queue[0][0]  # for sibling open
            else:
                element.tail = '\n' + indent * (level - 1)  # for parent close
            queue[0:0] = children  # prepend so children come before siblings


def _create_token_object(sentence_data, sentence_object, number, word_string):
    for token_data in sentence_data:
        token = ET.SubElement(sentence_object, 'tok')
        _create_orth_and_lex_objects(token_data, token, number, word_string)


def _create_orth_and_lex_objects(token_data, token_object, number, word_string):
    orth = ET.SubElement(token_object, 'orth')
    lex = ET.SubElement(token_object, 'lex')
    base = ET.SubElement(lex, 'base')
    ctag = ET.SubElement(lex, 'ctag')
    orth.text = token_data.split(' ')[0]
    base.text = token_data.split(' ')[0]
    ctag.text = token_data.split(' ')[1]


def convert_tsv_to_xml():
    csv.field_size_limit(sys.maxsize)
    xml_doc = ET.Element('cesAna')
    xml_doc.set("xmlns:xlink", "http://www.w3.org/1999/xlink")
    chunk_list = ET.SubElement(xml_doc, 'chunkList')
    paragraph = ET.SubElement(chunk_list, 'chunk', id='ch1', type='p')
    create_xml_file(paragraph)
    prettify(xml_doc)
    tree = ET.ElementTree(xml_doc)
    tree.write('resources/example_0.xml', encoding="UTF-8", xml_declaration=True)


def create_xml_file(paragraph_object):
    # xml_doc = ET.Element('chunkList')
    # xml_doc.set("xmlns:xlink", "http://www.w3.org/1999/xlink")
    # paragraph = ET.SubElement(xml_doc, 'chunk', id='ch1', type='p')
    for sentence_data in read_sentence_from_tsv():
        sentence_object = ET.SubElement(paragraph_object, 'sentence')
        _create_token_object(sentence_data, sentence_object, 1, 'This')
    # for row in rows:
    #     _create_token_object(sentence_object, 1, 'This')
    # _create_token_object(sentence, 2, 'is')
    # _create_token_object(sentence, 3, 'first')
    # _create_token_object(sentence, 4, 'example')
    # _create_token_object(sentence, 5, 'sentence')
    # _create_token_object(sentence, 6, '.')
    # prettify(xml_doc)
    # tree = ET.ElementTree(xml_doc)
    # tree.write('resources/example_1.xml', encoding="UTF-8", xml_declaration=True)


def read_sentence_from_tsv():
    with open("resources/taggers/example-pos/it-1/test.tsv") as fd:
        rd = csv.reader(fd, delimiter="\t")
        sentence = []
        for row in rd:
            # print(row)
            if row:
                sentence.append(row[0])
            else:
                yield sentence
                # create_xml_file(rows)
                sentence.clear()
            # print(row[0].split(" ")[0])


def main():
    convert_tsv_to_xml()
    # read_tsv()
    # create_xml_files()


if __name__ == '__main__':
    main()
