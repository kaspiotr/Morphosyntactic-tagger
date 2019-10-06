import argparse
import xml.etree.ElementTree as ET
from utils.classes import Paragraph, Sentence, Token
from utils.handle_file_io_operations import write_dicts_from_xmls_in_directory_to_jsonlines_file

ns = {'cor': '{http://www.tei-c.org/ns/1.0}',
      'nkjp': '{http://www.nkjp.pl/ns/1.0}',
      'xi': '{http://www.w3.org/2001/XInclude}'}


def parse_xml(file_path):
    """Parses all ann_morphosyntax.xml files from nkjp corpus

    Parameters
    ----------
    file_path : str
        The file location of the *.xml file to be parsed

    Yields
    ------
    Paragraph
        an object of Paragraph type

    """
    global token, sentence, paragraph, interps_base_form, interps_part_of_speech
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
                            if subelement[0].text is not None:
                                interps_base_form = subelement[0].text
                            else:
                                interps_base_form = ""
                        if subelement.get('name') == "ctag":
                            interps_part_of_speech = subelement[0].get('value')
                        if subelement.get('name') == "msd":
                            for proposed_tag_element in list(subelement[0].iter(ns.get('cor') + 'symbol')):
                                if proposed_tag_element.get('value') != "":
                                    token.add_proposed_tags(interps_base_form + ":" + interps_part_of_speech + ":" + proposed_tag_element.get('value'))
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="The absolute path with name of the saved *jsonl file.", type=str)
    parser.add_argument("-NKJP_dir_path", help="The absolute path to the directory with NKJP corpora.",
                        default='/resources/NKJP-PodkorpusMilionowy-1.2/', type=str)
    args = parser.parse_args()
    write_dicts_from_xmls_in_directory_to_jsonlines_file(parse_xml, args.file_path, args.NKJP_dir_path)


if __name__ == '__main__':
    main()
