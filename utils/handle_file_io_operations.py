import glob
import errno
import jsonlines

nkjp_directory_path = '/home/kaspiotr/Dev/MorphosyntacticTagger/resources/NKJP-PodkorpusMilionowy-1.2/'
jsonl_output_file_path = '/home/kaspiotr/Dev/MorphosyntacticTagger/resources/'
maca_output_xml_file_path = '/home/kaspiotr/Dev/MorphosyntacticTagger/resources/maca_output/maca_out.xml'


def write_dicts_from_xmls_in_directory_to_jsonlines_file(parsing_generator, output_file_name, directory_path=nkjp_directory_path, output_file_path=jsonl_output_file_path):
    path = directory_path + '*/' + 'ann_morphosyntax.xml'
    xml_files = glob.iglob(path)
    file_path_with_name_and_ext = output_file_path + output_file_name + '.jsonl'
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


def fetch_maca_input_from_xml_files_in_directory(parsing_generator, directory_path=nkjp_directory_path):
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
    with jsonlines.open(jsonl_file_path, mode='r') as reader:
        for nkjp_json in reader:
            paragraph_str = ""
            for sentences in nkjp_json['sentences']:
                for sentence in sentences['sentence']:
                    paragraph_str = append_token(paragraph_str, sentence['token'])
            yield (paragraph_str, '-'.join(sentence['token']['id'].split('-')[:-2]))


def write_dict_from_xml_with_maca_output_to_jsonlines_file(paragraph_id, parsing_generator, output_file_name, input_xml_file_path=maca_output_xml_file_path, output_file_path=jsonl_output_file_path):
    file_path_with_name_and_ext = output_file_path + output_file_name + '.jsonl'
    with jsonlines.open(file_path_with_name_and_ext, mode='a') as writer:
        try:
            with open(input_xml_file_path):
                for next_paragraph in parsing_generator(input_xml_file_path):
                    writer.write(next_paragraph.create_paragraph_dict(paragraph_id))
        except IOError as exec:
            if exec.errno != errno.EISDIR:
                raise


def append_token(paragraph_str, token):
    paragraph_str += token['changed_form'] if token['separator'] else ' ' + token['changed_form']
    return paragraph_str
