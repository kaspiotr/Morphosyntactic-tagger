import jsonlines
import os
import json

maca_output_jsonl_file_path = '/home/kaspiotr/Dev/MorphosyntacticTagger/resources/maca_output.jsonl'
nkjp_output_jsonl_file_path = '/home/kaspiotr/Dev/MorphosyntacticTagger/resources/nkjp_output.jsonl'
id2pos_in_nkjp_file = {}


def populate_dicts_with_id2pos_mapping(id2pos_in_nkjp_file_dict):
    with open(nkjp_output_jsonl_file_path, mode='rb') as nkjp_fh:
        with jsonlines.open(nkjp_output_jsonl_file_path) as nkjp_reader:
            for nkjp_json in nkjp_reader:
                id2pos_in_nkjp_file_dict[nkjp_json['id']] = {"first_byte_pos": nkjp_fh.tell()}
                nkjp_fh.readline()


def print_paragraphs_with_different_sentence_no_between_maca_and_nkjp():
    with open(nkjp_output_jsonl_file_path, mode='rb') as nkjp_fh:
        with jsonlines.open(maca_output_jsonl_file_path) as maca_reader:
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


def main():
    populate_dicts_with_id2pos_mapping(id2pos_in_nkjp_file)
    print_paragraphs_with_different_sentence_no_between_maca_and_nkjp()


if __name__ == '__main__':
    main()
