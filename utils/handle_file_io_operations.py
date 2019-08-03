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
                nkjp_directory_id = xml_file_name.split('/')[-2]
                for plain_text in parsing_generator(xml_file_name):
                    yield (plain_text, nkjp_directory_id)
        except IOError as exec:
            if exec.errno != errno.EISDIR:
                raise


def write_dict_from_xml_with_maca_output_to_jsonlines_file(directory_id, parsing_generator, output_file_name, input_xml_file_path=maca_output_xml_file_path, output_file_path=jsonl_output_file_path):
    file_path_with_name_and_ext = output_file_path + output_file_name + '.jsonl'
    with jsonlines.open(file_path_with_name_and_ext, mode='a') as writer:
        try:
            with open(input_xml_file_path):
                idx = 1
                for next_paragraph in parsing_generator(input_xml_file_path):
                    writer.write(next_paragraph.create_paragraph_dict(directory_id + '-' + str(idx)))
                    idx += 1
        except IOError as exec:
            if exec.errno != errno.EISDIR:
                raise
