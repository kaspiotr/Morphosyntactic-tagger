import xml.etree.ElementTree as ET
from utils.classes import Paragraph, Sentence, Token

xml_file_path = '/home/kaspiotr/Dev/MorphosyntacticTagger/resources/NKJP-PodkorpusMilionowy-1.2/010-2-000000001/ann_morphosyntax.xml'
xml_file_path2 = '/home/kaspiotr/Dev/MorphosyntacticTagger/resources/NKJP-PodkorpusMilionowy-1.2/030-2-000000009/ann_morphosyntax.xml'
xml_file_path3 = '/home/kaspiotr/Dev/MorphosyntacticTagger/resources/train-gold.xml'

paragraphs = []


def add_paragraph(paragraph):
    paragraphs.append(paragraph)


def parse_xml(file_path):
    # root = ET.parse(xml_file_path).getroot().getchildren()[1].getchildren()[1].getchildren()
    for event, element in ET.iterparse(file_path, events=("end",)):
        raw_tag = element.tag
        if "{" in element.tag:
            raw_tag = element.tag.replace(element.tag[element.tag.find("{"): element.tag.find("}")+1], '')
        # print(element.tag[element.tag.find("{"): element.tag.find("}")+1])
        if event == "end" and raw_tag == "p":  # use "p" to parse paragraphs in xml files form NKJP, "chunk" to parse chunks from Poleval 2017
            paragraph = Paragraph(element.tag)
            #  paragraph_printout = "Paragraph: " + element.tag
            for child in list(element):
                sentence = Sentence(child.tag)
                for grandchild in list(child):
                    token = Token(grandchild.tag)
                    token.add_changed_form(grandchild[0][0][0].text)
                    for grand_x2_child in list(grandchild[0]):
                        if grand_x2_child.get('name') == 'interps':
                            print(grand_x2_child.attrib)
                            for grand_x3_child in grand_x2_child:
                                if grand_x3_child.get('type') == 'lex':
                                    print("\t-", grand_x3_child.attrib)
                                    for grand_x4_child in grand_x3_child:
                                        print("\t\t-", grand_x4_child.attrib)
                                        if grand_x4_child.get('name') == 'base':
                                            token.add_base_form(grand_x4_child[0].text)
                                        if grand_x4_child.get('name') == 'msd':
                                            print("\t\t\t-", grand_x4_child[0].tag)
                                            for grand_x6_child in grand_x4_child[0]:
                                                print("\t\t\t\t-", grand_x6_child.get('value'))
                                                token.add_proposed_tags(grand_x6_child.get('value'))
                        if grand_x2_child.get('name') == 'disamb':
                            print(grand_x2_child.attrib)
                            for grand_x3_child in grand_x2_child:
                                print("\t-", grand_x3_child.attrib)
                                for grand_x4_child in grand_x3_child:
                                    print("\t\t-", grand_x4_child.attrib)
                                    if grand_x4_child.get('name') == 'interpretation':
                                        print("\t\t\t-", grand_x4_child[0].text)
                                        token.add_tag(grand_x4_child[0].text)

                    sentence.add_token(token)
                paragraph.add_sentence(sentence)
            add_paragraph(paragraph)
            yield paragraph
            element.clear()


def main():
    for next_paragraph in parse_xml(xml_file_path):
        print("Paragraph: ", next_paragraph.paragraph_tag)
        for sentence in next_paragraph.sentences:
            print("\tSentence: ", sentence.sentence_tag)
            for token in sentence.tokens:
                print("\t\tToken: ", token.token_tag)
                print("\t\t\t-changed form: ", token.changed_form)
                print("\t\t\t-base form: ", token.base_form)
                print("\t\t\t-tag: ", token.tag)
                print("\t\t\t-proposed tags: ")
                for proposed_tag in token.proposed_tags:
                    print("\t\t\t\t-", proposed_tag)


if __name__ == '__main__':
    main()
