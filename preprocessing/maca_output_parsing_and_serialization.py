import xml.etree.ElementTree as ET
import errno
from subprocess import Popen, PIPE
from utils.handle_file_io_operations import fetch_maca_input_from_xml_files_in_directory, write_dict_from_xml_with_maca_output_to_jsonlines_file
from utils.classes import Paragraph, Sentence, Token

nkjp_direcotry_path = '/home/kaspiotr/Dev/MorphosyntacticTagger/resources/NKJP-PodkorpusMilionowy-1.2/'
output_file_path = '/home/kaspiotr/Dev/MorphosyntacticTagger/resources/'
output_maca_xml_file_path = '/home/kaspiotr/Dev/MorphosyntacticTagger/resources/maca_output/maca_out.xml'


ns = {'cor': '{http://www.tei-c.org/ns/1.0}',
      'xi': '{http://www.w3.org/2001/XInclude}'}


def parse_maca_input_from_xml_files_in_directory(file_path):
    for event, element in ET.iterparse(file_path, events=("end",)):
        if element.tag == ns.get('cor') + 'div':
            paragraph_text = ""
            first_subelement = True
            for subelement in element:
                if first_subelement:
                    first_subelement = False
                else:
                    paragraph_text += " "
                paragraph_text += subelement.text
            yield paragraph_text


def _maca(input, output_xml_file_path):
    cmd = ['maca-analyse', '-qs', 'morfeusz2-nkjp', '-o', 'ccl']
    p = Popen(cmd, stdout=PIPE, stdin=PIPE, universal_newlines=True)
    stdout = p.communicate(input=input)[0]
    try:
        p.stdin.close()
    except BrokenPipeError:
        pass
    p.wait()
    if p.returncode != 0:
        raise Exception('Maca is not working properly')
    try:
        with open(output_xml_file_path, mode='w') as writer:
            writer.write(stdout)
    except IOError as exec:
        if exec.errno != errno.EISDIR:
            raise


def create_xml_file_from_maca_output(output_xml_file_path):
    for (maca_input, nkjp_directory_id_with_paragraph_id) in fetch_maca_input_from_xml_files_in_directory(parse_maca_input_from_xml_files_in_directory):
        _maca(maca_input, output_xml_file_path)
        yield nkjp_directory_id_with_paragraph_id


def parse_xml(file_path):
    """Parses  maca_out.xml file with output generated from maca

    Parameters
    ----------
        file_path : str
            The file location of the *.xml file to be parsed

        Yields
        ------
        Paragraph
            an object of Paragraph type

    """
    for event, element in ET.iterparse(file_path, events=("start", "end",)):
        if event == "start":
            if element.tag == "chunk":
                paragraph = Paragraph(element.tag)
            if element.tag == "sentence":
                sentence = Sentence(element.tag)
            if element.tag == "tok":
                token = Token(element.tag)
        if event == "end":
            if element.tag == "tok":
                token.add_changed_form(element[0].text)
                sentence.add_token(token)
                for subelement in element:
                    if subelement.tag == "lex":
                        interps_base_form = subelement[0].text.split(':')[0]
                        morph_interp = subelement[1].text
                        token.add_proposed_tags(interps_base_form + ":" + morph_interp)
                        token.add_base_form(interps_base_form)
                        token.add_tag(morph_interp)
            if element.tag == "sentence":
                paragraph.add_sentence(sentence)
            if element.tag == "chunk":
                yield paragraph
                element.clear()


def main():
    for paragraph_id in create_xml_file_from_maca_output(output_maca_xml_file_path):
        write_dict_from_xml_with_maca_output_to_jsonlines_file(paragraph_id, parse_xml, 'maca_output')


if __name__ == '__main__':
    main()

