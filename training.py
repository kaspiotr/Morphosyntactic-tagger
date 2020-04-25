from flair.data import Corpus
from flair.datasets import ColumnCorpus
from flair.embeddings import FlairEmbeddings, StackedEmbeddings, TokenEmbeddings, OneHotEmbeddings
from sklearn.model_selection import StratifiedKFold
from typing import List
import os
import jsonlines
import numpy as np
import re
import errno
import shutil
import flair
import sys


def _count_occurs(key, dictionary):
    if key in dictionary:
        dictionary[key] += 1
    else:
        dictionary[key] = 1


def map_paragraph_id_to_text_category_name(paragraph, text_cat_to_no_of_els):
    """
    Converts paragraph id (<NKJP corpora directory id>+_+<no of paragraph in that directory>)
    to text category name that is useful to derive text classes and use them for instance
    in stratified k-fold cross-validation.
    Populates text_cat_to_no_of_els dictionary for that text category.

    :param paragraph: JSON object of paragraph
    :param text_cat_to_no_of_els: dictionary: key - text category name, value - number of elements in this category
    :return: text category name in a form of a string
    """
    paragraph_id = paragraph["id"]
    if re.match("^BienczykPrzezroczystosc", paragraph_id):
        _count_occurs("BienczykPrzezroczystosc", text_cat_to_no_of_els)
        return "BienczykPrzezroczystosc"
    if re.match("^BrukowiecOchlanski", paragraph_id):
        _count_occurs("BrukowiecOchlanski", text_cat_to_no_of_els)
        return "BrukowiecOchlanski"
    if re.match("^BrzezickiNocunBialorus", paragraph_id):
        _count_occurs("BrzezickiNocunBialorus", text_cat_to_no_of_els)
        return "BrzezickiNocunBialorus"
    if re.match(r"^DP\d{4}", paragraph_id):
        _count_occurs("DP", text_cat_to_no_of_els)
        return "DP"
    if re.match("^EkspressWieczorny", paragraph_id):
        _count_occurs("EkspressWieczorny", text_cat_to_no_of_els)
        return "EkspressWieczorny"
    if re.match(r"^forumowisko.pl_\d+", paragraph_id):
        _count_occurs("forumowisko.pl", text_cat_to_no_of_els)
        return "forumowisko.pl"
    if re.match("^GazetaGoleniowska", paragraph_id):
        _count_occurs("GazetaGoleniowska", text_cat_to_no_of_els)
        return "GazetaGoleniowska"
    if re.match("^GazetaKociewska", paragraph_id):
        _count_occurs("GazetaKociewska", text_cat_to_no_of_els)
        return "GazetaKociewska"
    if re.match("^GazetaLubuska", paragraph_id):
        _count_occurs("GazetaLubuska", text_cat_to_no_of_els)
        return "GazetaLubuska"
    if re.match("^GazetaMalborska", paragraph_id):
        _count_occurs("GazetaMalborska", text_cat_to_no_of_els)
        return "GazetaMalborska"
    if re.match("^GazetaPomorska", paragraph_id):
        _count_occurs("GazetaPomorska", text_cat_to_no_of_els)
        return "GazetaPomorska"
    if re.match("^GazetaTczewska", paragraph_id):
        _count_occurs("GazetaTczewska", text_cat_to_no_of_els)
        return "GazetaTczewska"
    if re.match("^GazetaWroclawska", paragraph_id):
        _count_occurs("GazetaWroclawska", text_cat_to_no_of_els)
        return "GazetaWroclawska"
    if re.match("^GlosPomorza", paragraph_id):
        _count_occurs("GlosPomorza", text_cat_to_no_of_els)
        return "GlosPomorza"
    if re.match("^GlosSzczecinski", paragraph_id):
        _count_occurs("GlosSzczecinski", text_cat_to_no_of_els)
        return "GlosSzczecinski"
    if re.match("^GraczykTropem", paragraph_id):
        _count_occurs("GraczykTropem", text_cat_to_no_of_els)
        return "GraczykTropem"
    if re.match("^GrzegorczykObogatym", paragraph_id):
        _count_occurs("GrzegorczykObogatym", text_cat_to_no_of_els)
        return "GrzegorczykObogatym"
    if re.match("^HellerPodgladanie", paragraph_id):
        _count_occurs("HellerPodgladanie", text_cat_to_no_of_els)
        return "HellerPodgladanie"
    if re.match("^IsakowiczZaleskiMoje", paragraph_id):
        _count_occurs("IsakowiczZaleskiMoje", text_cat_to_no_of_els)
        return "IsakowiczZaleskiMoje"
    if re.match("^KolakowskiOco", paragraph_id):
        _count_occurs("KolakowskiOco", text_cat_to_no_of_els)
        return "KolakowskiOco"
    if re.match("^KOT", paragraph_id):
        _count_occurs("KOT", text_cat_to_no_of_els)
        return "KOT"
    if re.match("^IsakowiczZaleskiMoje", paragraph_id):
        _count_occurs("IsakowiczZaleskiMoje", text_cat_to_no_of_els)
        return "IsakowiczZaleskiMoje"
    if re.match("^KurierKwidzynski", paragraph_id):
        _count_occurs("KurierKwidzynski", text_cat_to_no_of_els)
        return "KurierKwidzynski"
    if re.match("^KurierSzczecinski", paragraph_id):
        _count_occurs("KurierSzczecinski", text_cat_to_no_of_els)
        return "KurierSzczecinski"
    if re.match("^KurierSzczecinski", paragraph_id):
        _count_occurs("KurierSzczecinski", text_cat_to_no_of_els)
        return "KurierSzczecinski"
    if re.match("^LukasiewiczRubryka", paragraph_id):
        _count_occurs("LukasiewiczRubryka", text_cat_to_no_of_els)
        return "LukasiewiczRubryka"
    if re.match("^LukaszewskiCel", paragraph_id):
        _count_occurs("LukaszewskiCel", text_cat_to_no_of_els)
        return "LukaszewskiCel"
    if re.match("^LukaszewskiOpolsce", paragraph_id):
        _count_occurs("LukaszewskiOpolsce", text_cat_to_no_of_els)
        return "LukaszewskiOpolsce"
    if re.match("^MentzelWszystkie", paragraph_id):
        _count_occurs("MentzelWszystkie", text_cat_to_no_of_els)
        return "MentzelWszystkie"
    if re.match("^Midrasz", paragraph_id):
        _count_occurs("Midrasz", text_cat_to_no_of_els)
        return "Midrasz"
    if re.match("^MysliwskiKamien", paragraph_id):
        _count_occurs("MysliwskiKamien", text_cat_to_no_of_els)
        return "MysliwskiKamien"
    if re.match("^MysliwskiTraktat", paragraph_id):
        _count_occurs("MysliwskiTraktat", text_cat_to_no_of_els)
        return "MysliwskiTraktat"
    if re.match("^NeckaCzlowiek", paragraph_id):
        _count_occurs("NeckaCzlowiek", text_cat_to_no_of_els)
        return "NeckaCzlowiek"
    if re.match("^NIE", paragraph_id):
        _count_occurs("NIE", text_cat_to_no_of_els)
        return "NIE"
    if re.match("^NowackaAs", paragraph_id):
        _count_occurs("NowackaAs", text_cat_to_no_of_els)
        return "NowackaAs"
    if re.match("^NowackaMale", paragraph_id):
        _count_occurs("NowackaMale", text_cat_to_no_of_els)
        return "NowackaMale"
    if re.match("^NowaTrybunaOpolska", paragraph_id):
        _count_occurs("NowaTrybunaOpolska", text_cat_to_no_of_els)
        return "NowaTrybunaOpolska"
    if re.match("^Rzeczpospolita", paragraph_id):
        _count_occurs("Rzeczpospolita", text_cat_to_no_of_els)
        return "Rzeczpospolita"
    if re.match("^SikoraMiedzy", paragraph_id):
        _count_occurs("SikoraMiedzy", text_cat_to_no_of_els)
        return "SikoraMiedzy"
    if re.match("^SlowoPowszechne", paragraph_id):
        _count_occurs("SlowoPowszechne", text_cat_to_no_of_els)
        return "SlowoPowszechne"
    if re.match("^StempowskiZapiski", paragraph_id):
        _count_occurs("StempowskiZapiski", text_cat_to_no_of_els)
        return "StempowskiZapiski"
    if re.match("^SuperExpress", paragraph_id):
        _count_occurs("SuperExpress", text_cat_to_no_of_els)
        return "SuperExpress"
    if re.match("^SzczeklikKore", paragraph_id):
        _count_occurs("SzczeklikKore", text_cat_to_no_of_els)
        return "SzczeklikKore"
    if re.match("^SzejnertCzarny", paragraph_id):
        _count_occurs("SzejnertCzarny", text_cat_to_no_of_els)
        return "SzejnertCzarny"
    if re.match("^Sztafeta", paragraph_id):
        _count_occurs("Sztafeta", text_cat_to_no_of_els)
        return "Sztafeta"
    if re.match("^TochmanCorenka", paragraph_id):
        _count_occurs("TochmanCorenka", text_cat_to_no_of_els)
        return "TochmanCorenka"
    if re.match("^TochmanWsciekly", paragraph_id):
        _count_occurs("TochmanWsciekly", text_cat_to_no_of_els)
        return "TochmanWsciekly"
    if re.match("^TomaszewskaJasnosc", paragraph_id):
        _count_occurs("TomaszewskaJasnosc", text_cat_to_no_of_els)
        return "TomaszewskaJasnosc"
    if re.match("^TomaszewskaTrojkat", paragraph_id):
        _count_occurs("TomaszewskaTrojkat", text_cat_to_no_of_els)
        return "TomaszewskaTrojkat"
    if re.match("^TrybunaLudu_Trybuna", paragraph_id):
        _count_occurs("TrybunaLudu_Trybuna", text_cat_to_no_of_els)
        return "TrybunaLudu_Trybuna"
    if re.match("^TrybunaSlaska", paragraph_id):
        _count_occurs("TrybunaSlaska", text_cat_to_no_of_els)
        return "TrybunaSlaska"
    if re.match("^WachKazdy", paragraph_id):
        _count_occurs("WachKazdy", text_cat_to_no_of_els)
        return "WachKazdy"
    if re.match("^WilkDom", paragraph_id):
        _count_occurs("WilkDom", text_cat_to_no_of_els)
        return "WilkDom"
    if re.match("^WilkWilczy", paragraph_id):
        _count_occurs("WilkWilczy", text_cat_to_no_of_els)
        return "WilkWilczy"
    if re.match("^ZycieINowoczesnosc", paragraph_id):
        _count_occurs("ZycieINowoczesnosc", text_cat_to_no_of_els)
        return "ZycieINowoczesnosc"
    if re.match("^ZycieWarszawy_Zycie", paragraph_id):
        _count_occurs("ZycieWarszawy_Zycie", text_cat_to_no_of_els)
        return "ZycieWarszawy_Zycie"
    if re.match(r"^\d{3}-\d{1}-\d{6,9}", paragraph_id):
        text_category = get_text_categories_from_nkjp_numbers_indices(paragraph_id)
        _count_occurs(text_category, text_cat_to_no_of_els)
        return text_category


"""
Description of classification used in below function can be found in file 'system_identyfikatorow.txt'
"""


def get_text_categories_from_nkjp_numbers_indices(text_id):
    """
    Creates text category name basing on NKJP corpora directories indices described in file 'system_identyfikatorow.txt'

    :param text_id: paragraph id in format <NKJP corpora directory id>+_+<no of paragraph in that directory>
    :return: text category name in form of a string
    """
    text_category = ""
    text_category = map_first_section_of_nkjp_numbers_indeces(text_id, text_category)
    text_category = map_second_section_of_nkjp_numbers_indices(text_id, text_category)
    return text_category


def map_first_section_of_nkjp_numbers_indeces(text_id, text_category):
    """
    Maps first three digits of NKJP corpora directory name into text category

    :param text_id: NKJP corpora paragraph id (in format: <NKJP corpora directory id>+_+<no of paragraph in that directory>)
    :param text_category: name of NKJP corpora text category in a form of a string
    :return: name of NKJP corpora text category in a form of a string
    """
    if re.match(r"^0\d\d", text_id):  # HTCT - Hard To Classify Texts (PL: Trudne w klasyfikacji (000-099))
        text_category += "HTCT"
        if re.match("^010", text_id):
            return text_category + "_undefined"  # undefined (PL: 010 Niezidentyfikowany)
        if re.match("^030", text_id):
            return text_category + "_oldie"  # oldie (PL: 030 Staroc)
        if re.match("^040", text_id):
            return  text_category + "_unclassified" # unclassified (PL: 040 Nieklasyfikowany)
    if re.match(r"^1\d\d", text_id):  # journalism (PL: Publicystyka (100-199))
        text_category += "journalism"
        if re.match("^110", text_id):
            return text_category + "_book"  # book (PL: 110 Ksiazka)
        if re.match("^120", text_id):
            return text_category + "_periodicals"  # periodicals (PL: 120 Periodyki)
        if re.match("^130", text_id):
            return text_category + "_journals"  # journals (PL: 130 Dzienniki)
    if re.match("^200", text_id):
        return text_category + "fiction"  # fiction (PL: 200 Beletrystyka)
    if re.match("^310", text_id):
        return text_category + "non-fiction"  # non-fiction (PL: 310 Literatura faktu)
    if re.match("^320", text_id):
        return text_category + "scientific_and_didactic"  # scientific and didactic (PL: 320 Naukowo-dydaktyczny)
    if re.match("^330", text_id):  # information and advisory services (PL: 330 Informacyjno-Poradnikowy)
        text_category += "information_and_advisory_services"
        return text_category
    if re.match(r"^6\d\d", text_id):
        text_category += "others"  # others (PL: Inne (600-699)
        if re.match("^610", text_id):
            return text_category + "_applied"  # applied (PL: 610 Użytkowe)
        if re.match("^611", text_id): # letters (PL: 611 Listy)
            text_category += "_letters"
            return text_category
        if re.match("^620", text_id): # internet (PL: 620 Internet)
            text_category += "_internet"
            return text_category
    if re.match(r"^7\d\d", text_id):
        text_category += "spoken"  # spoken (PL: Mówione (770-799))
        if re.match("^710", text_id):
            return text_category + "_written_down"  # written down (PL: 710 Spisane)
        if re.match("^711", text_id):
            return text_category + "_written_down_from_radio"  # written down from radio (PL: 711 Spisane-Radio)
        if re.match("^712", text_id):  # written down parliament and senate (PL: 712 Spisane-Sejm+Senat)
            return text_category + "_written_down_parliament_and_senate"
        if re.match("^720", text_id):
            return text_category + "_conversation"  # written conversation (PL: 720 Konwersacyjne)


def map_second_section_of_nkjp_numbers_indices(text_id, text_category):
    """
    Maps forth sign of NKJP corpora
    paragraph id (made of digits, that has format <NKJP corpora directory id>+_+<no of paragraph in that directory>)
    to text category name

    :param text_id: NKJP corpora paragraph id (<NKJP corpora directory id>+_+<no of paragraph in that directory>)
    :param text_category: name of NKJP corpora text category in a form of a string
    :return: name of NKJP corpora text category in a form of a string
    """
    if re.match(r"^\d\d\d-1", text_id):
        return text_category + "_IPI"
    if re.match(r"^\d\d\d-2", text_id):
        return text_category + "_PWN"
    if re.match(r"^\d\d\d-3", text_id):
        return text_category + "_Pelcra"
    if re.match(r"^\d\d\d-4", text_id):
        return text_category + "_IJP"
    if re.match(r"^\d\d\d-5", text_id):
        return text_category + "_D_Lewandowska_PHD_Thesis"  # Doktorat Doroty Lewandowskiej (gotowe próbki prasowe)


def write_to_file(file_name, content):
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    try:
        with open(file_name, mode='a') as writer:
            writer.write(content)
    except IOError as exec:
        if exec.errno != errno.EISDIR:
            raise


def remove_data_directory_with_content(directory_path):
    shutil.rmtree(directory_path)


def _get_proposed_tag_str(proposed_tag):
    return proposed_tag["tag"]


def _write_paragraph_to_file(paragraphs_np_array, paragraphs_indexes, destination_file_name, is_test_set=True):
    sentences_no = 0
    sentences_that_match_no = 0
    for paragraph_json_idx in paragraphs_indexes:
        for sentence in paragraphs_np_array.item(paragraph_json_idx)["sentences"]:
            sentences_no += 1
            if is_test_set or sentence["match"]:
                sentences_that_match_no += 1
                for token in sentence["sentence"]:
                    token_json = token["token"]
                    write_to_file(destination_file_name, token_json["changed_form"] + " " + token_json["tag"]
                                  + " " + str(token_json["separator"]) + " "
                                  + ";".join(map(lambda proposed_tag: proposed_tag["tag"], token_json["proposed_tags"]))
                                  + "\n")
                write_to_file(destination_file_name, "\n")
    print("Total number of sentences in NKJP corpora: %s " % sentences_no)
    print("No. of sentences that match in terms of tokenisation between NKJP corpora and MACA analyzer: %s " % sentences_that_match_no)


def train(jsonl_file):
    """
    Trains a sequence labeling model using stratified 10-fold cross-validation, which means that model is trained for
    each division of corpora into test and train data (dev data are sampled from train data) (preserving the percentage
    of samples for each class).
    Model is trained to predict part of speech tag and takes into account information about:
    - text (plain text made of tokens that together form a sentence),
    - occurrence of separator before token,
    - proposed tags for given token.
    It is trained with use of Stacked Embeddings used to combine different embeddings together. Words are embedded
    using a concatenation of two vector embeddings:
    - Flair Embeddings - contextual string embeddings that capture latent syntactic-semantic
      information that goes beyond standard word embeddings. Key differences are: (1) they are trained without any
      explicit notion of words and thus fundamentally model words as sequences of characters. And (2) they are
      contextualized by their surrounding text, meaning that the same word will have different embeddings depending on
      its contextual use.
      There are forward (that goes through the given on input plain text form left to right) and backward model (that
      goes through the given on input plain text form right to left) used for part of speech (pos) tag training.
    - One Hot Embeddings - embeddings that encode each word in a vocabulary as a one-hot vector, followed by an
      embedding layer. These embeddings thus do not encode any prior knowledge as do most other embeddings. They also
      differ in that they require to see a Corpus during instantiation, so they can build up a vocabulary consisting of
      the most common words seen in the corpus, plus an UNK token for all rare words.
      There are two One Hot Embeddings used in training:
      - first to embed information about occurrence of separator before token,
      - second to embed information about concatenated with a ';' proposed tags.
    Model and training logs are saved in resources/taggers/example-pos directory.

    :param jsonl_file: file in *.jsonl format with paragraphs in a form of a JSON in each line
    """
    maca_output_serialized_from_nkjp_marked_file = os.path.dirname(os.path.abspath(__file__)) + '/output/' + jsonl_file + '.jsonl'
    # this is the folder in which train and test files reside
    data_folder = os.path.dirname(os.path.abspath(__file__)) + '/data'
    train_file_name = data_folder + "/train"
    test_file_name = data_folder + "/test"
    with jsonlines.open(maca_output_serialized_from_nkjp_marked_file) as reader:
        text_category_to_number_of_elements = {}
        paragraphs_X = []
        paragraph_text_category_y = []
        for paragraph in reader:
            paragraphs_X.append(paragraph)
            paragraph_text_category_y.append(map_paragraph_id_to_text_category_name(paragraph, text_category_to_number_of_elements))
        X = np.array(paragraphs_X)
        y = np.array(paragraph_text_category_y)
        skf = StratifiedKFold(n_splits=10)
        print("Number of paragraphs of each text category\n")
        print("%-50s%s" % ("Text category", "paragraphs number"))
        for text_cat, els_no in text_category_to_number_of_elements.items():
            print("%-50s%s" % (text_cat, els_no))
        for train_index, test_index in skf.split(X, y):
            _write_paragraph_to_file(X, train_index, train_file_name, False)
            _write_paragraph_to_file(X, test_index, test_file_name)
            # define columns
            columns = {0: 'text', 1: 'pos', 3: 'is_separator', 4: 'proposed_tags'}
            # init a corpus using column format, data folder and the names of the train and test files
            # 1. get the corpus
            corpus: Corpus = ColumnCorpus(data_folder, columns,
                                          train_file='train',
                                          test_file='test',
                                          dev_file=None)
            print(corpus)
            # len(corpus.train)
            # print(corpus.train[0].to_tagged_string('pos'))
            # print("TRAIN:", train_index, "TEST:", test_index)
            # 2. what tag do we want to predict
            tag_type = 'pos'
            # 3. make the tag dictionary from the corpus
            tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)
            print(tag_dictionary)
            # 4. initialize embeddings
            embedding_types: List[TokenEmbeddings] = [
                FlairEmbeddings('news-forward', chars_per_chunk=64),
                FlairEmbeddings('news-backward', chars_per_chunk=64),
                OneHotEmbeddings(corpus=corpus, field='is_separator'),
                OneHotEmbeddings(corpus=corpus, field='proposed_tags'),
            ]
            embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)
            # 5. initialize sequence tagger
            from flair.models import SequenceTagger
            tagger: SequenceTagger = SequenceTagger(hidden_size=256,
                                                    embeddings=embeddings,
                                                    tag_dictionary=tag_dictionary,
                                                    tag_type=tag_type,
                                                    use_crf=True)
            # 6. initialize trainer
            from flair.trainers import ModelTrainer

            trainer: ModelTrainer = ModelTrainer(tagger, corpus)

            # 7. start training
            trainer.train('resources/taggers/example-pos',
                          learning_rate=0.1,
                          mini_batch_size=32,
                          embeddings_storage_mode='gpu',
                          max_epochs=sys.maxsize,
                          monitor_test=True)
            # 8. plot weight traces (optional)
            from flair.visual.training_curves import Plotter
            plotter = Plotter()
            plotter.plot_weights('resources/taggers/example-pos/weights.txt')
            remove_data_directory_with_content(data_folder)


def main():
    print(flair.device)
    train('maca_output_marked')


if __name__ == '__main__':
    main()
