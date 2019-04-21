import xml.etree.ElementTree as ET
import glob
import errno
from utils.classes import Paragraph, Sentence, Token

ns = {'cor': '{http://www.tei-c.org/ns/1.0}',
      'nkjp': '{http://www.nkjp.pl/ns/1.0}',
      'xi': '{http://www.w3.org/2001/XInclude}'}

nkjp_direcotry_path = '/home/kaspiotr/Dev/MorphosyntacticTagger/resources/NKJP-PodkorpusMilionowy-1.2/'
output_file_path = '/home/kaspiotr/Dev/MorphosyntacticTagger/resources/'


def parse_xml(file_path):
    global token, sentence, paragraph, interps_base_form
    for event, element in ET.iterparse(file_path, events=("start", "end",)):
        if event == "start":
            if element.tag == ns.get('cor') + 'p':
                paragraph = Paragraph(element.tag)
            if element.tag == ns.get('cor') + 's':
                sentence = Sentence(element.tag)
            if element.tag == ns.get('cor') + 'f' and element.get('name') == "orth":
                token = Token(element.tag)
        if event == "end":
            if element.tag == ns.get('cor') + 'f':
                if element.get('name') == "orth":
                    token.add_changed_form(element[0].text)
                    sentence.add_token(token)
                if element.get('name') == "nps":
                    token.add_separator(True)
                if element.get('name') == "interps":
                    for subelement in list(element.iter(ns.get('cor') + 'f')):
                        if subelement.get('name') == "base":
                            interps_base_form = subelement[0].text
                        if subelement.get('name') == "msd":
                            for proposed_tag_element in list(subelement[0].iter(ns.get('cor') + 'symbol')):
                                if proposed_tag_element.get('value') != "":
                                    token.add_proposed_tags(interps_base_form + ":" + proposed_tag_element.get('value'))
                                else:
                                    token.add_proposed_tags(interps_base_form)
                if element.get('name') == "disamb":
                    disamb_base_form_with_tag = element[0][1][0].text.split(":")
                    token.add_base_form(disamb_base_form_with_tag[0])
                    token.add_tag(":".join(disamb_base_form_with_tag[1:]))
            if element.tag == ns.get('cor') + 's':
                paragraph.add_sentence(sentence)
            if element.tag == ns.get('cor') + 'p':
                yield paragraph
                element.clear()


def write_str_to_jsonl_file(path, file_name, data):
    file_path_with_name_and_ext = path + file_name + '.jsonl'
    with open(file_path_with_name_and_ext, 'a') as writer:
        writer.write(data)
        writer.write('\n')


def write_str_from_xmls_in_directory(directory_path, output_file_path, output_file_name):
    path = directory_path + '*/' +'ann_morphosyntax.xml'
    xml_files = glob.glob(path)
    for xml_file_name in xml_files:
        try:
            with open(xml_file_name) as f:
                for next_paragraph in parse_xml(xml_file_name):
                    write_str_to_jsonl_file(output_file_path, output_file_name, next_paragraph.create_paragraph_line_string())
        except IOError as exc:
            if exc.errno != errno.EISDIR:
                raise


def main():
    write_str_from_xmls_in_directory(nkjp_direcotry_path, output_file_path, 'test_output')


if __name__ == '__main__':
    main()
