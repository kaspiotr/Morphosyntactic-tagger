import unittest
import jsonlines

maca_output_jsonl_file_path = '/home/kaspiotr/Dev/MorphosyntacticTagger/resources/output_maca.jsonl'
nkjp_output_jsonl_file_path = '/home/kaspiotr/Dev/MorphosyntacticTagger/resources/TEST_output_nkjp.jsonl'


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
                    self.assertMultiLineEqual(json[0]['sentences'][0]['sentence'][0]['token']['changed_form'], json[1]['sentences'][0]['sentence'][0]['token']['changed_form'])


if '__name__' == '__main__':
    unittest.main()
