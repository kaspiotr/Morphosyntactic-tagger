import jsonlines
import logging as log
import os

maca_and_nkjp_output_merge_jsonl_file_path = \
    '/home/kaspiotr/Dev/MorphosyntacticTagger/output/maca_output_marked.jsonl'


def log_info_from_maca_and_nkjp_output_merge_jsonl_file(maca_and_nkjp_output_merge):
    """
    Logs information included in maca_output_marked.jsonl like:
     - how many sentences from the MACA have the same tokenization as in the NKJP corpora
     - how many sentences from the MACA have different tokenization from the one
       that is in the NKJP corpora
     - how many tokens have base_form and tag taken from the NKJP corpora
     - how many tokens have base_form and tag set to 'ign' (it was impossible to
       take base_form and tag for them from the NKJP corpora)
    and writes those information in maca_and_nkjp_tokens_merge_info.log file in output directory of this project

    :param nkjp_output_jsonl_file_path: str
        The absolute path to the *.jsonl file where data serialized from NKJP corpora are stored.
    :param maca_output_jsonl_file_path: str
        The absolute path to the *.jsonl file where data serialized from MACA output are stored.
    """
    log.basicConfig(filename='output/maca_and_nkjp_tokens_merge_info.log', format='%(levelname)s:%(message)s', level=log.INFO)
    if maca_and_nkjp_output_merge is None:
        maca_and_nkjp_output_merge = os.path.dirname(os.path.abspath(__file__)) + '/output/maca_output_marked.jsonl'
    with jsonlines.open(maca_and_nkjp_output_merge) as reader:
        log.info("Information about input training file maca_output_marked.jsonl")
        total_maca_sentences_no = 0
        maca_sentences_with_the_same_tokenization_as_in_nkjp_no = 0
        maca_sentences_with_different_tokenization_than_in_nkjp_no = 0
        total_maca_tokens_no = 0
        tokens_with_ign_tag_and_base_form_no = 0
        tokens_with_tag_and_base_form_set_from_nkjp_no = 0
        for paragraph_json in reader:
            for sentence_json in paragraph_json['sentences']:
                total_maca_sentences_no += 1
                if sentence_json['match']:
                    maca_sentences_with_the_same_tokenization_as_in_nkjp_no += 1
                else:
                    maca_sentences_with_different_tokenization_than_in_nkjp_no += 1
                for token_json in sentence_json['sentence']:
                    total_maca_tokens_no += 1
                    if token_json['token']['tag'] == 'ign':
                        tokens_with_ign_tag_and_base_form_no += 1
                    else:
                        tokens_with_tag_and_base_form_set_from_nkjp_no += 1
        log.info("Total no. of MACA sentences: %s" % total_maca_sentences_no)
        log.info("No. of sentences with the same tokenization between the NKJP and the MACA: %s"
                 % maca_sentences_with_the_same_tokenization_as_in_nkjp_no)
        log.info("No. of sentences with different tokenization between the NKJP and the MACA: %s"
                 % maca_sentences_with_different_tokenization_than_in_nkjp_no)
        log.info("Total no. of MACA tokens: %s" % total_maca_tokens_no)
        log.info("No. of MACA tokens with tag and base_form set from the NKJP corpora: %s"
                 % tokens_with_tag_and_base_form_set_from_nkjp_no)
        log.info("No. of MACA tokens with 'ign' tag and base_form: %s"
                 % tokens_with_ign_tag_and_base_form_no)


def main():
    log_info_from_maca_and_nkjp_output_merge_jsonl_file(maca_and_nkjp_output_merge_jsonl_file_path)


if __name__ == '__main__':
    main()
