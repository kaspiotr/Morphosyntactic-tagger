import jsonlines

maca_output_jsonl_file_path = '/home/kaspiotr/Dev/MorphosyntacticTagger/resources/output_maca.jsonl'
nkjp_output_jsonl_file_path = '/home/kaspiotr/Dev/MorphosyntacticTagger/resources/output_nkjp.jsonl'


def print_lines_of_nkjp_and_maca_jsonl_files_that_have_different_changed_forms():
    line_number = 1
    with jsonlines.open(maca_output_jsonl_file_path) as maca_reader:
        with jsonlines.open(nkjp_output_jsonl_file_path) as nkjp_reader:
            print("Differences in changed form:")
            for json in zip(maca_reader, nkjp_reader):
                if json[0]['sentence'][0]['token'][0]['changed_form'] != json[1]['sentence'][0]['token'][0]['changed_form']:
                    print("Line no. %s: maca: %s, nkjp: %s" % (line_number, json[0]['sentence'][0]['token'][0]['changed_form'], json[1]['sentence'][0]['token'][0]['changed_form']))
                line_number += 1


def main():
    print_lines_of_nkjp_and_maca_jsonl_files_that_have_different_changed_forms()


if __name__ == '__main__':
    main()
