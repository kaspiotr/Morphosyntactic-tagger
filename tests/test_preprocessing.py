import unittest
import jsonlines

maca_output_jsonl_file_path = '/home/kaspiotr/Dev/MorphosyntacticTagger/resources/maca_output_serialized_from_nkjp.jsonl'
maca_output_from_plain_nkjp_text_jsonl_file_path = '/home/kaspiotr/Dev/MorphosyntacticTagger/resources/maca_output.jsonl'
nkjp_output_jsonl_file_path = '/home/kaspiotr/Dev/MorphosyntacticTagger/resources/nkjp_output.jsonl'
maca_and_nkjp_output_merge_jsonl_file_path = '/home/kaspiotr/Dev/MorphosyntacticTagger/output/maca_output_marked_test.jsonl'


class TestPreprocessing(unittest.TestCase):

    # given__when__then
    def test_nkjp_and_maca_jsonl_files__create__same_length(self):
        maca_output_jsonl_file_line_no = 0
        nkjp_output_jsonl_file_line_no = 0
        with jsonlines.open(maca_output_jsonl_file_path) as reader:
            for _ in reader:
                maca_output_jsonl_file_line_no += 1

        with jsonlines.open(nkjp_output_jsonl_file_path) as reader:
            for _ in reader:
                nkjp_output_jsonl_file_line_no += 1

        self.assertEqual(maca_output_jsonl_file_line_no, nkjp_output_jsonl_file_line_no)

    def test_nkjp_and_maca_jsonl_files__create__corresponding_jsons_in_the_same_lines(self):
        with jsonlines.open(maca_output_jsonl_file_path) as maca_reader:
            with jsonlines.open(nkjp_output_jsonl_file_path) as nkjp_reader:
                for json in zip(maca_reader, nkjp_reader):
                    self.assertMultiLineEqual(json[0]['sentences'][0]['sentence'][0]['token']['changed_form'],
                                              json[1]['sentences'][0]['sentence'][0]['token']['changed_form'])

    def test_maca_and_nkjp_output_merge__create__all_base_forms_and_tags_for_sentences_with_consistent_tokenization_between_maca_and_nkjp(self):
        with jsonlines.open(maca_and_nkjp_output_merge_jsonl_file_path) as reader:
            for paragraph_json in reader:
                for sentence_json in paragraph_json['sentences']:
                    for token_json in sentence_json['sentence']:
                        if token_json['token']['base_form'] != 'ign':
                            self.assertEqual('TEST_BASE_FORM', token_json['token']['base_form'], "base_form not set for token with id "
                                             + token_json['token']['id'])
                        if token_json['token']['tag'] != 'ign':
                            self.assertEqual('TEST_TAG', token_json['token']['tag'], "tag not set for token with id "
                                             + token_json['token']['id'])

    def test_maca_and_nkjp_output_merge__create__all_base_forms_and_tags_with_ign_value_in_sentences_with_different_tokenization_between_maca_and_nkjp(self):
        with jsonlines.open(maca_and_nkjp_output_merge_jsonl_file_path) as reader:
            for paragraph_json in reader:
                for sentence_json in paragraph_json['sentences']:
                    for token_json in sentence_json['sentence']:
                        if token_json['token']['base_form'] == 'ign':
                            self.assertEqual(False, sentence_json['match'],
                                             "sentence with id " + sentence_json['id']
                                             + " not set as not matching (as the one with different tokenisation than in NKJP) for token with id "
                                             + token_json['token']['id'] + " although token's base_form is set to 'ign'")
                        if token_json['token']['tag'] == 'ign':
                            self.assertEqual(False, sentence_json['match'],
                                             "sentence with id " + sentence_json['id']
                                             + " not set as not matching (as the one with different tokenisation than in NKJP) for token with id "
                                             + token_json['token']['id'] + " although token's tag is set to 'ign'")

    def test_maca_output_serialized_from_nkjp__create__all_base_form_and_tags_are_set_as_ign(self):
        with jsonlines.open(maca_output_jsonl_file_path) as reader:
            for paragraph_json in reader:
                for sentence_json in paragraph_json['sentences']:
                    for token_json in sentence_json['sentence']:
                        self.assertEqual('ign', token_json['token']['base_form'], "base_form not set for token with id "
                                         + token_json['token']['id'])
                        self.assertEqual('ign', token_json['token']['tag'], "tag not set for token with id "
                                         + token_json['token']['id'])

    def test_maca_output_from_plain_nkjp_text__create__all_base_form_and_tags_are_set_as_ign(self):
        with jsonlines.open(maca_output_from_plain_nkjp_text_jsonl_file_path) as reader:
            for paragraph_json in reader:
                for sentence_json in paragraph_json['sentences']:
                    for token_json in sentence_json['sentence']:
                        self.assertEqual('ign', token_json['token']['base_form'], "base_form not set for token with id "
                                         + token_json['token']['id'])
                        self.assertEqual('ign', token_json['token']['tag'], "tag not set for token with id "
                                         + token_json['token']['id'])


if '__name__' == '__main__':
    unittest.main()
