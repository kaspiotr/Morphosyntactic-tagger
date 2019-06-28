import glob
import errno
import jsonlines

nkjp_direcotry_path = '/home/kaspiotr/Dev/MorphosyntacticTagger/resources/NKJP-PodkorpusMilionowy-1.2/'
output_file_path = '/home/kaspiotr/Dev/MorphosyntacticTagger/resources/'


def write_dicts_from_xmls_in_directory_to_jsonlines_file(parsing_generator, output_file_name, directory_path=nkjp_direcotry_path, output_file_path_par=output_file_path):
    path = directory_path + '*/' + 'ann_morphosyntax.xml'
    xml_files = glob.iglob(path)
    file_path_with_name_and_ext = output_file_path_par + output_file_name + '.jsonl'
    with jsonlines.open(file_path_with_name_and_ext, mode='a') as writer:
        for xml_file_name in xml_files:
            try:
                with open(xml_file_name):
                    for next_paragraph in parsing_generator(xml_file_name):
                        writer.write(next_paragraph.create_paragraph_dict())
            except IOError as exec:
                if exec.errno != errno.EISDIR:
                    raise
