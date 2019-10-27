import argparse
import jsonlines
import os
import json
from utils.handle_file_io_operations import append_token

id2pos_in_nkjp_file = {}
id2pos_in_maca_file = {}


def populate_dicts_with_id2pos_mapping(id2pos_in_nkjp_file_dict, id2pos_in_maca_file_dict, nkjp_output_jsonl_file_path, maca_output_jsonl_file_path):
    """
    Populates dictionaries given by parameters id2pos_in_nkjp_file_dict and id2pos_in_maca_file_dict that allow to map *jsonl files lines with paragraph id

    Parameters
    ----------
    id2pos_in_nkjp_file_dict: dictionary
        The dictionary that maps paragraph id to its position in *.jsonl file with paragraphs serialized from NKJP corpora.
    id2pos_in_maca_file_dict: dictionary
        The dictionary that maps paragraph id to its position in *.jsonl file with paragraphs gained from MACA analyzer output.
    nkjp_output_jsonl_file_path: str
        The absolute path to the *.jsonl file where data serialized from NKJP corpora are stored.
    maca_output_jsonl_file_path: str
        The absolute path to the *.jsonl file where data serialized from MACA output are stored.
    """
    if nkjp_output_jsonl_file_path is None:
        nkjp_output_jsonl_file_path = os.path.dirname(os.path.abspath(__file__)) + '/resources/nkjp_output.jsonl'
    with open(nkjp_output_jsonl_file_path, mode='rb') as nkjp_fh, \
            jsonlines.open(nkjp_output_jsonl_file_path) as nkjp_reader:
        for nkjp_json in nkjp_reader:
            id2pos_in_nkjp_file_dict[nkjp_json['id']] = {"first_byte_pos": nkjp_fh.tell()}
            nkjp_fh.readline()
    if maca_output_jsonl_file_path is None:
        maca_output_jsonl_file_path = os.path.dirname(os.path.abspath(__file__)) + '/resources/maca_output.jsonl'
    with open(maca_output_jsonl_file_path, mode='rb') as maca_fh, \
            jsonlines.open(maca_output_jsonl_file_path) as maca_reader:
        for maca_json in maca_reader:
            id2pos_in_maca_file_dict[maca_json['id']] = {"first_byte_pos": maca_fh.tell()}
            maca_fh.readline()


def print_paragraphs_with_different_sentence_no_between_maca_and_nkjp(nkjp_output_jsonl_file_path, maca_output_jsonl_file_path):
    """
    Prints paragraphs that have been separated into different number of sentences in NKJP corpora and by MACA analyzer

    Parameters
    ----------
    nkjp_output_jsonl_file_path: str
        The absolute path to the *.jsonl file where data serialized from NKJP corpora are stored.
    maca_output_jsonl_file_path: str
        The absolute path to the *.jsonl file where data serialized from MACA output are stored.
    """
    if nkjp_output_jsonl_file_path is None:
        nkjp_output_jsonl_file_path = os.path.dirname(os.path.abspath(__file__)) + '/resources/nkjp_output.jsonl'
    if maca_output_jsonl_file_path is None:
        maca_output_jsonl_file_path = os.path.dirname(os.path.abspath(__file__)) + '/resources/maca_output.jsonl'
    with open(nkjp_output_jsonl_file_path, mode='rb') as nkjp_fh, \
            jsonlines.open(maca_output_jsonl_file_path) as maca_reader:
        print("Differences between maca and nkjp jsons:")
        maca_sentences_no = 0
        maca_paragraph_no = 0
        nkjp_sentences_no = 0
        nkjp_paragraph_no = 0
        for maca_json in maca_reader:
            nkjp_fh.seek(id2pos_in_nkjp_file[maca_json['id']]['first_byte_pos'], os.SEEK_SET)
            nkjp_json = json.loads(nkjp_fh.readline().decode('utf-8'))
            maca_paragraph_no += 1
            for _ in maca_json['sentences']:
                maca_sentences_no += 1
            nkjp_paragraph_no += 1
            for _ in nkjp_json['sentences']:
                nkjp_sentences_no += 1
            if maca_sentences_no != nkjp_sentences_no:
                print("Paragraph no.: %d, sentences no.: maca: %d, nkjp: %d" % (nkjp_paragraph_no, maca_sentences_no, nkjp_sentences_no))
            maca_sentences_no = 0
            nkjp_sentences_no = 0


def populate_buffers(maca_output_marked_jsonl_file_path, nkjp_output_jsonl_file_path, maca_output_jsonl_file_path):
    """
    Populates buffers used in align algorithm

    Parameters
    ----------
    maca_output_marked_jsonl_file_path: str
        The absolute path to the file *.jsonl where similarities between NKJP and MACA will be marked or just name of that file.
    nkjp_output_jsonl_file_path: str
        The absolute path to the *.jsonl file where data serialized from NKJP corpora are stored.
    maca_output_jsonl_file_path: str
        The absolute path to the *.jsonl file where data serialized from MACA output are stored.
    """
    if len(maca_output_marked_jsonl_file_path.split('/')) == 1:
        maca_output_marked_jsonl_file_path = os.path.abspath(
            os.path.dirname(os.path.abspath(__file__))) + '/output/' + maca_output_marked_jsonl_file_path
    if nkjp_output_jsonl_file_path is None:
        nkjp_output_jsonl_file_path = os.path.dirname(os.path.abspath(__file__)) + '/resources/nkjp_output.jsonl'
    if maca_output_jsonl_file_path is None:
        maca_output_jsonl_file_path = os.path.dirname(os.path.abspath(__file__)) + '/resources/maca_output.jsonl'
    with open(nkjp_output_jsonl_file_path, mode='rb') as nkjp_fh, \
            jsonlines.open(maca_output_jsonl_file_path) as maca_reader, \
            jsonlines.open(maca_output_marked_jsonl_file_path + '.jsonl', mode='w') as maca_writer:
        paragraph_no = 1
        for maca_json in maca_reader:
            nkjp_fh.seek(id2pos_in_nkjp_file[maca_json['id']]['first_byte_pos'], os.SEEK_SET)
            nkjp_json = json.loads(nkjp_fh.readline().decode('utf-8'))
            maca_paragraph_buffer = []
            nkjp_paragraph_buffer = []
            for maca_sentences in maca_json['sentences']:
                for maca_sentence in maca_sentences['sentence']:
                    maca_paragraph_buffer.append(maca_sentence['token'])
            for nkjp_sentences in nkjp_json['sentences']:
                for nkjp_sentence in nkjp_sentences['sentence']:
                    nkjp_paragraph_buffer.append(nkjp_sentence['token'])
            print("Paragraph no.: %d" % paragraph_no)
            print("Maca list length: %s" % len(maca_paragraph_buffer))
            print("NKJP list length: %s" % len(nkjp_paragraph_buffer))
            paragraph_no += 1
            align(maca_json, nkjp_paragraph_buffer, maca_paragraph_buffer)
            maca_writer.write(maca_json)


def align(maca_json, nkjp_buffer, maca_buffer):
    """
    Align algorithm that marks similarities between NKJP and MACA analyzer output POS tagging
    maca_json: json file
        The file of *.json type where algorithm marks if there is similarity or not in POS tagging between NKJP and MACA analyzer
    nkjp_buffer: list of str
        The buffer with NKJP paragraph in form of a list of strings
    maca_buffer: list of str
        The buffer with paragprahs of NKJP corpora returned by MACA analyzer in form of a list of strings
    """
    nkjp_paragraph_str = ""
    maca_paragraph_str = ""
    prev_maca_token = None
    curr_maca_token = None
    sentence_no = 0
    while nkjp_buffer or maca_buffer:
        if len(nkjp_paragraph_str) == len(maca_paragraph_str):
            if nkjp_paragraph_str != maca_paragraph_str:
                print("Alignment error")
                break
            prev_maca_token = curr_maca_token
            curr_maca_token = maca_buffer.pop(0)
            if prev_maca_token is not None and prev_maca_token['id'].split('-')[-2] != curr_maca_token['id'].split('-')[-2]:
                maca_json['sentences'][sentence_no]['match'] = True
                sentence_no += 1
            nkjp_paragraph_str = append_token(nkjp_paragraph_str, nkjp_buffer.pop(0))
            maca_paragraph_str = append_token(maca_paragraph_str, curr_maca_token)
        elif len(nkjp_paragraph_str) < len(maca_paragraph_str):
            if not nkjp_buffer:
                break
            nkjp_paragraph_str = append_token(nkjp_paragraph_str, nkjp_buffer.pop(0))
        else:
            if not maca_buffer:
                break
            prev_maca_token = curr_maca_token
            curr_maca_token = maca_buffer.pop(0)
            if prev_maca_token is not None and prev_maca_token['id'].split('-')[-2] != curr_maca_token['id'].split('-')[-2]:
                maca_json['sentences'][sentence_no]['match'] = True
                sentence_no += 1
            maca_paragraph_str = append_token(maca_paragraph_str, curr_maca_token)

    if prev_maca_token is not None and prev_maca_token['id'].split('-')[-2] != curr_maca_token['id'].split('-')[-2]:
        maca_json['sentences'][sentence_no]['match'] = True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("MACA_marked_file", help="The absolute path to the file *.jsonl where similarities between NKJP and MACA will be marked or just name of that file", type=str)
    parser.add_argument("-NKJP_file", help="The absolute path to the *.jsonl file where data serialized from NKJP corpora are stored.", type=str)
    parser.add_argument("-MACA_file", help="The absolute path to the *.jsonl file where data serialized from MACA output are stored.", type=str)

    args = parser.parse_args()
    populate_dicts_with_id2pos_mapping(id2pos_in_nkjp_file, id2pos_in_maca_file, args.NKJP_file, args.MACA_file)
    print_paragraphs_with_different_sentence_no_between_maca_and_nkjp(args.NKJP_file, args.MACA_file)
    populate_buffers(args.MACA_marked_file, args.NKJP_file, args.MACA_file)


if __name__ == '__main__':
    main()
