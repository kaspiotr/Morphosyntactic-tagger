import os
import glob
import errno
import jsonlines


def write_dicts_from_xmls_in_directory_to_jsonlines_file(parsing_generator, output_file_path, dir_path):
    """
    Creates *.jsonl file with data serialized from the *.xml files in the NKJP corpora

    Parameters
    ----------
    parsing_generator: generator
        The generator used to parse ann_morphosyntax.xml files from NKJP corpora.
    output_file_path: str
        The absolute path with name of the saved *jsonl file or just the name of that file.
    dir_path: str
        The absolute path to the directory with NKJP corpora.

    Raises
    ------
    IOError
        If file ann_morphosyntax.xml is not found in specified dir_path
    """
    if dir_path == '/resources/NKJP-PodkorpusMilionowy-1.2/':
        my_path = '/'.join(os.path.abspath(os.path.dirname(os.path.abspath(__file__))).split('/')[:-1])
    else:
        my_path = ''
    path = str(my_path) + str(dir_path) + '*/' + 'ann_morphosyntax.xml'
    if 'NKJP-PodkorpusMilionowy-1.2' not in os.listdir('/'.join(path.split('/')[:-3])):
        raise IOError("Contents of directory named NKJP-PodkorpusMilionowy-1.2 not found in the specified location.")
    xml_files = glob.iglob(path)
    if len(output_file_path.split('/')) == 1:
        output_file_path = '/'.join(os.path.abspath(os.path.dirname(os.path.abspath(__file__))).split('/')[:-1]) + '/resources/' + output_file_path
    file_path_with_name_and_ext = output_file_path + '.jsonl'
    with jsonlines.open(file_path_with_name_and_ext, mode='a') as writer:
        for xml_file_name in xml_files:
            try:
                with open(xml_file_name):
                    idx = 1
                    directory_id = xml_file_name.split('/')[-2]
                    for next_paragraph in parsing_generator(xml_file_name):
                        writer.write(next_paragraph.create_paragraph_dict(directory_id + '-' + str(idx)))
                        idx += 1
            except IOError as exec:
                if exec.errno != errno.EISDIR:
                    raise


def fetch_maca_input_from_xml_files_in_directory(parsing_generator, directory_path):
    """
    Fetches input for MACA analyzer from text.xml files available in NKJP corpora

    Parameters
    ----------
    parsing_generator: generator
        Generator that parses all ann_morphosyntax.xml files from NKJP corpora and yields
    directory_path: str
        The absolute path to the directory with NKJP corpora.

    Yields
    ------
    Yields a tuple with plain text and NKJP corpora paragraph id
    """
    path = directory_path + '*/' + 'text.xml'
    xml_files = glob.iglob(path)
    for xml_file_name in xml_files:
        try:
            with open(xml_file_name):
                idx = 1
                nkjp_directory_id = xml_file_name.split('/')[-2]
                for plain_text in parsing_generator(xml_file_name):
                    yield (plain_text, nkjp_directory_id + '-' + str(idx))
                    idx += 1
        except IOError as exec:
            if exec.errno != errno.EISDIR:
                raise


def serialize_maca_input_from_nkjp_jsonl(jsonl_file_path):
    """
    Serializes input for MACA analyzer from *.jsonl with paragraphs (in each line) serialized from the NKJP corpora

    Parameters
    ----------
    jsonl_file_path: str
        The path to the *.jsonl file where data serialized from NKJP corpora are stored.

    Yields
    ------
    A tuple with paragraph plain text in form of a string (that can be used as MACA analyzer input) and NKJP directory id with paragraph id
    """
    with jsonlines.open(jsonl_file_path, mode='r') as reader:
        for nkjp_json in reader:
            paragraph_str = ""
            for sentences in nkjp_json['sentences']:
                for sentence in sentences['sentence']:
                    paragraph_str = append_token(paragraph_str, sentence['token'])
            yield (paragraph_str, '-'.join(sentence['token']['id'].split('-')[:-2]))


def write_dict_from_xml_with_maca_output_to_jsonlines_file(paragraph_id, parsing_generator, output_file_path):
    """
    Fetches data from maca_out.xml file and writes to the *.jsonl file defined by output_file_path parameter

    Parameters
    ----------
    paragraph_id: str
        String that describes paragraph id of the NKJP corpora that is just written to the output *.jsonl file
    parsing_generator: generator
        The generator that parses maca_out.xml file with output gained from MACA analyzer
    output_file_path: str
        The absolute path to the *.jsonl file where data from MACA analyze based on NKJP plain text will be saved or just the name of that file.

    Raises
    ------
    IOError
        If file maca_out.xml is not found
    """
    input_xml_file_path = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-1]) + '/resources/maca_output/maca_out.xml'
    if len(output_file_path.split('/')) == 1:
        output_file_path = '/'.join(os.path.abspath(os.path.dirname(os.path.abspath(__file__))).split('/')[:-1]) + '/resources/' + output_file_path
    file_path_with_name_and_ext = output_file_path + '.jsonl'
    with jsonlines.open(file_path_with_name_and_ext, mode='a') as writer:
        try:
            with open(input_xml_file_path):
                for next_paragraph in parsing_generator(input_xml_file_path):
                    writer.write(next_paragraph.create_paragraph_dict(paragraph_id))
        except IOError as exec:
            if exec.errno != errno.EISDIR:
                raise


def append_token(paragraph_str, token):
    """
    Appends token with or without space to the paragraph string

    Parameters
    ----------
    paragraph_str: str
        String with paragraph plain text constructed to that point
    token: Token
        The object that represents a token from *.jsonl file

    Returns
    -------
    Paragraph text in a from of a string
    """
    paragraph_str += token['changed_form'] if token['separator'] else ' ' + token['changed_form']
    return paragraph_str
