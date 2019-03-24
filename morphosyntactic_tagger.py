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
                    token.add_changed_form(grandchild[0][0][0])
                    # if grandchild[0][0][0].text is not ',' and grandchild[0][0][0].text is not '.':
                    #     token.add_base_form(grandchild[0][1][0][0][0])
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
                print("\t\t\t-changed form: ", token.changed_form.text)
                # if token.base_form is not None:
                #     print("\t\t\t-base form: ", token.base_form.text)


if __name__ == '__main__':
    main()
