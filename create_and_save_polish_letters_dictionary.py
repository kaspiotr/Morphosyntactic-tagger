from flair.data import Dictionary
from training import use_scratch_dir_if_available


def create_local_polish_letters_dictionary_based_on_common(dictionary_name):
    dictionary = Dictionary.load(name="chars")
    dictionary.add_item('Ą')
    dictionary.add_item('ą')
    dictionary.add_item('Ć')
    dictionary.add_item('ć')
    dictionary.add_item('Ę')
    dictionary.add_item('ę')
    dictionary.add_item('Ł')
    dictionary.add_item('ł')
    dictionary.add_item('Ń')
    dictionary.add_item('ń')
    dictionary.add_item('Ó')
    dictionary.add_item('ó')
    dictionary.add_item('Ś')
    dictionary.add_item('ś')
    dictionary.add_item('Ź')
    dictionary.add_item('ź')
    dictionary.add_item('Ż')
    dictionary.add_item('ż')
    dictionary.save(use_scratch_dir_if_available('resources/' + dictionary_name))


def main():
    create_local_polish_letters_dictionary_based_on_common('polish_letters_dict')


if __name__ == '__main__':
    main()

