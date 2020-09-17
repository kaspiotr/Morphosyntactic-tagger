import argparse
import re
import xml.etree.ElementTree as ET
from utils.classes import Paragraph, Sentence, Token
from utils.handle_file_io_operations import write_dicts_from_xmls_in_directory_to_jsonlines_file

ns = {'cor': '{http://www.tei-c.org/ns/1.0}',
      'nkjp': '{http://www.nkjp.pl/ns/1.0}',
      'xi': '{http://www.w3.org/2001/XInclude}'}

base_form_part_with_pos_tag_regex = '[a-z0-9A-Z\/]+(:[a-z0-9]+)*$'
nkjp_pos_allowed_base_forms_regex = r"[a-zA-Z0-9ąćęłńóśźżĄĆĘŁŃÓŚŹŻ\"\'!?.,;\-\s„”–()&*…—§’/ü\[\]+­“°%é=ôòéëä•ţ@‘ö×·$" \
                                    r"_{}«»~èàášíúČ#¨˝ý><ÉŢő−č|`řñç^âêōěßû]+(:[a-z0-9]+)*"
nkjp_base_form_first_emoji_regex = "^:[-]?[DOP\/]:"
nkjp_base_form_second_emoji_regex = "^[:(][-oP]?[\/()\\|\]:]?"
nkjp_websites_base_forms_first_regex = "\s*http://"
nkjp_websites_base_forms_second_regex = "news:"


def correct_nkjp_base_form_and_tag_format(base_form_with_tag):
    """
    Handles proper base_form and tag parsing from ann_morphosyntax.xml NKJP corpora files

    :param base_form_with_tag: str
        base_form and tag of NKJP corpora token divided with ':'
    :return: tuple (str, str)
        A tuple of two strings: (base_form, tag)
    """
    if re.fullmatch(nkjp_pos_allowed_base_forms_regex, base_form_with_tag) is None:
        if base_form_with_tag == '::interp':
            return ':', 'interp'
        if re.findall(nkjp_base_form_first_emoji_regex, base_form_with_tag):
            tag = ":".join(re.search(base_form_part_with_pos_tag_regex, base_form_with_tag).group().split(':')[1:])
            base_form = base_form_with_tag[0:len(base_form_with_tag) - len(tag) - 1]
            return base_form, tag
        if re.findall(nkjp_base_form_second_emoji_regex, base_form_with_tag):
            tag = re.search(base_form_part_with_pos_tag_regex, base_form_with_tag).group()
            base_form = base_form_with_tag[0:len(base_form_with_tag) - len(tag) - 1]
            return base_form, tag
        if re.findall(nkjp_websites_base_forms_first_regex, base_form_with_tag) \
                or re.findall(nkjp_websites_base_forms_second_regex, base_form_with_tag):
            tag = ":".join(re.search(base_form_part_with_pos_tag_regex, base_form_with_tag).group().split(':')[1:])
            base_form = base_form_with_tag[0:len(base_form_with_tag) - len(tag) - 1]
            return base_form, tag
        if base_form_with_tag.startswith("E:") or base_form_with_tag.startswith("D:"):
            base_form = base_form_with_tag[0:2]
            tag = base_form_with_tag[3:]
            return base_form, tag
        if base_form_with_tag == '\\:interp':
            return '\\', 'interp'
        if base_form_with_tag == '´:interp':
            return '´', 'interp'
    else:
        base_form = base_form_with_tag.split(':')[0]
        tag = ":".join(base_form_with_tag.split(':')[1:])
        return base_form, tag


def parse_xml(file_path):
    """
    Parses all ann_morphosyntax.xml files from NKJP corpora

    :param file_path: str
        The file location of the *.xml file to be parsed
    :yields Paragraph:
        An object of Paragraph type
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
                    token.add_separator(False)
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
                                token.add_proposed_tags(interps_base_form + ":" + interps_part_of_speech + ":"
                                                        + proposed_tag_element.get('value'))
                if element.get('name') == "disamb":
                    base_form, tag = correct_nkjp_base_form_and_tag_format(element[0][1][0].text)
                    token.add_base_form(base_form)
                    token.add_tag(tag)
            if element.tag == ns.get('cor') + 's':
                paragraph.add_sentence(sentence)
            if element.tag == ns.get('cor') + 'p':
                yield paragraph
                element.clear()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="The absolute path with name of the saved *jsonl file or just the name of "
                                          "that file.", type=str)
    parser.add_argument("-NKJP_dir_path", help="The absolute path to the directory with NKJP corpora.",
                        default='/resources/NKJP-PodkorpusMilionowy-1.2/', type=str)
    args = parser.parse_args()
    write_dicts_from_xmls_in_directory_to_jsonlines_file(parse_xml, args.file_path, args.NKJP_dir_path)


if __name__ == '__main__':
    main()
