import argparse
import errno
import os
import xml.etree.ElementTree as ET
from subprocess import Popen, PIPE
from utils.classes import Paragraph, Sentence, Token
from utils.handle_file_io_operations import fetch_maca_input_from_xml_files_in_directory, write_dict_from_xml_with_maca_output_to_jsonlines_file, serialize_maca_input_from_nkjp_jsonl


ns = {'cor': '{http://www.tei-c.org/ns/1.0}',
      'xi': '{http://www.w3.org/2001/XInclude}'}


def parse_maca_input_from_xml_files_in_directory(file_path):
    """
    Parses all text.xml files from NKJP corpora directory

    :param file_path: str
        The absolute path to the directory with NKJP corpora.
    :yields: Plain text with NKJP corpora paragraph
    """
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
    """
    Runs MACA analizer on a given by input parameter chunk of text and writes result to the file given by the output_xml_file_path parameter

    :param input: str
        Plain text that is an input to the MACA analyzer
    :param output_xml_file_path: str
        The absolute path to the *.jsonl file where output from MAC analyzer is going to be written
    :raises: Exception('Maca is not working properly')
        IOError
        If file maca_out.xml is not found
    """
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


def create_xml_file_from_maca_output(jsonl_file_path, nkjp_dir_path, serialize_from_nkjp_jsonl=False):
    """
    Runs MACA analyzer on a given chunk of plain text and saves it in the maca_out.xml file in resource/maca_output/
    directory of this project

    :param jsonl_file_path: str
        The path to the *.jsonl file where data serialized from NKJP corpora are stored.
    :param nkjp_dir_path: str
        The absolute path to the directory with NKJP corpora.
    :param serialize_from_nkjp_jsonl: boolean
        Flag that if is set to True will serialize input data for MACA analyser from indicated by nkjp_dir_path file
        or, if set to False, will collect input data for MACA analyser directly from text.xml files of NKJP corpora
        directories
    :yields nkjp_directory_id_with_paragraph_id: string
        Yields string that contains inkjp directory id concatenated with paragraph number
    """
    output_xml_file_path = os.path.dirname(os.path.abspath(__file__)) + '/resources/maca_output/maca_out.xml'
    if serialize_from_nkjp_jsonl:
        if jsonl_file_path is None:
            jsonl_file_path = os.path.dirname(os.path.abspath(__file__)) + '/resources/nkjp_output.jsonl'
        for (maca_input, nkjp_directory_id_with_paragraph_id) in serialize_maca_input_from_nkjp_jsonl(jsonl_file_path):
            _maca(maca_input, output_xml_file_path)
            yield nkjp_directory_id_with_paragraph_id
    else:
        if nkjp_dir_path == '/resources/NKJP-PodkorpusMilionowy-1.2/':
            my_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__))) + nkjp_dir_path
        else:
            my_path = nkjp_dir_path
        if 'NKJP-PodkorpusMilionowy-1.2' not in os.listdir('/'.join(my_path.split('/')[:-2])):
            raise IOError(
                "Contents of directory named NKJP-PodkorpusMilionowy-1.2 not found in the specified location.")
        for (maca_input, nkjp_directory_id_with_paragraph_id) in fetch_maca_input_from_xml_files_in_directory(parse_maca_input_from_xml_files_in_directory, my_path):
            _maca(maca_input, output_xml_file_path)
            yield nkjp_directory_id_with_paragraph_id


def parse_xml(file_path):
    """
    Parses maca_out.xml file with output gained from MACA analyzer

    :param file_path: str
        The file location of the *.xml file to be parsed.
    :yields Paragraph:
        An object of Paragraph type.
    """
    is_prev_el_tag_ns = False
    for event, element in ET.iterparse(file_path, events=("start", "end",)):
        if event == "start":
            if element.tag == "chunk":
                paragraph = Paragraph(element.tag)
            if element.tag == "sentence":
                sentence = Sentence(element.tag)
            if element.tag == "tok":
                token = Token(element.tag)
                if is_prev_el_tag_ns:
                    token.add_separator(False)
                    is_prev_el_tag_ns = False
            if element.tag == "ns":
                is_prev_el_tag_ns = True
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
                        token.add_tag('num' if morph_interp == 'num:::' else morph_interp)
            if element.tag == "sentence":
                paragraph.add_sentence(sentence)
            if element.tag == "chunk":
                yield paragraph
                element.clear()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("MACA_file", help="The absolute path to the *.jsonl file where data from MACA analyze based on NKJP plain text will be saved or just the name of that file.", type=str)
    parser.add_argument("MACA_serialized_file", help="The absolute path to the *.jsonl file where data serialized from file given by argument NKJP_file_path will be saved.", type=str)
    parser.add_argument("-NKJP_file_path", help="The path to the *.jsonl file where data serialized from NKJP corpora are stored.", type=str)
    parser.add_argument("-NKJP_dir_path", help="The absolute path to the directory with NKJP corpora.",
                        default='/resources/NKJP-PodkorpusMilionowy-1.2/', type=str)
    args = parser.parse_args()

    for paragraph_id in create_xml_file_from_maca_output(args.NKJP_file_path, args.NKJP_dir_path):
        write_dict_from_xml_with_maca_output_to_jsonlines_file(paragraph_id, parse_xml, args.MACA_file)
    for paragraph_id in create_xml_file_from_maca_output(args.NKJP_file_path, args.NKJP_dir_path, True):
        write_dict_from_xml_with_maca_output_to_jsonlines_file(paragraph_id, parse_xml, args.MACA_serialized_file)


if __name__ == '__main__':
    main()

