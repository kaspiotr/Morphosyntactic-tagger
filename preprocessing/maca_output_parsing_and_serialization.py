import subprocess
import xml.etree.ElementTree as ET
from utils.handle_file_io_operations import fetch_maca_input_from_xml_files_in_directory

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
                print(subelement.tag)
                paragraph_text += subelement.text
            yield paragraph_text


def create_xml_file_from_maca_output(output_xml_file_path):
    for maca_input in fetch_maca_input_from_xml_files_in_directory(parse_maca_input_from_xml_files_in_directory):
        cmd = maca_input + " | maca-analyse -qs morfeusz2-nkjp -o ccl > " + output_xml_file_path
        subprocess.call("echo " + cmd, shell=True)
        # cmd2 = maca_input + " | maca-analyse -qs morfeusz2-nkjp -o plain"
        # subprocess.call("echo " + cmd2, shell=True)
        yield


def main():
    for _ in create_xml_file_from_maca_output(output_maca_xml_file_path):
        print('plik utworzony')


if __name__ == '__main__':
    main()

