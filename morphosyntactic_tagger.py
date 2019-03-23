import xml.etree.ElementTree as ET

xml_file_path = '/home/kaspiotr/Dev/MorphosyntacticTagger/resources/NKJP-PodkorpusMilionowy-1.2/010-2-000000001/ann_morphosyntax.xml'
xml_file_path2 = '/home/kaspiotr/Dev/MorphosyntacticTagger/resources/NKJP-PodkorpusMilionowy-1.2/030-2-000000009/ann_morphosyntax.xml'
xml_file_path3 = '/home/kaspiotr/Dev/MorphosyntacticTagger/resources/train-gold.xml'


def parse_xml(file_path):
    # root = ET.parse(xml_file_path).getroot().getchildren()[1].getchildren()[1].getchildren()
    for event, element in ET.iterparse(file_path, events=("start", "end",)):
        raw_tag = element.tag
        if "{" in element.tag:
            raw_tag = element.tag.replace(element.tag[element.tag.find("{"): element.tag.find("}")+1], '')
        # print(element.tag[element.tag.find("{"): element.tag.find("}")+1])
        if event == "start" and raw_tag == "p":  # use "p" to parse paragraphs in xml files form NKJP, "chunk" to parse chunks from Poleval 2017
            paragraph = element.tag
            yield paragraph
        element.clear()


def main():
    for next_paragraph in parse_xml(xml_file_path):
        print(next_paragraph)


if __name__ == '__main__':
    main()
