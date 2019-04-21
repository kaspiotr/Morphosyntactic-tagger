import xml.etree.ElementTree as ET
import jsonlines
from utils.classes import Paragraph, Sentence, Token

ns = {'cor': '{http://www.tei-c.org/ns/1.0}',
      'nkjp': '{http://www.nkjp.pl/ns/1.0}',
      'xi': '{http://www.w3.org/2001/XInclude}'}

xml_file_path = '/home/kaspiotr/Dev/MorphosyntacticTagger/resources/NKJP-PodkorpusMilionowy-1.2/010-2-000000001/ann_morphosyntax.xml'


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


def write_to_jsonlines_file(path, file_name, data):
    file_path_with_name_and_ext = path + file_name + '.jsonl'
    with open(file_path_with_name_and_ext, 'a') as writer:
        writer.write(data)
        writer.write('\n')


def main():
    for next_paragraph in parse_xml(xml_file_path):
        write_to_jsonlines_file('./', 'out', next_paragraph.create_paragraph_line_string())
        print("Paragraph: ", next_paragraph.paragraph_tag)
        for sentence in next_paragraph.sentences:
            print("\tSentence: ", sentence.sentence_tag)
            for token in sentence.tokens:
                print("\t\tToken: ", token.token_tag)
                print("\t\t\t-changed form: ", token.changed_form)
                print("\t\t\t-base form: ", token.base_form)
                print("\t\t\t-tag: ", token.tag)
                print("\t\t\t-separator: ", token.separator)
                print("\t\t\t-proposed tags: ")
                for proposed_tag in token.proposed_tags:
                    print("\t\t\t\t-", proposed_tag)


if __name__ == '__main__':
    main()
