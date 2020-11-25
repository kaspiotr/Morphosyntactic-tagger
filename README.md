# Morphosyntactic-tagger
## Master thesis: Polish tagger based on contextual word embeddings

## Notices
* The 1-million-word subcorpus used in this project is available here:
[The manually annotated 1-million word subcorpus of the NJKP, available on GNU GPL v.3](http://clip.ipipan.waw.pl/NationalCorpusOfPolish?action=AttachFile&do=get&target=NKJP-PodkorpusMilionowy-1.2.tar.gz)
and should be downloaded and unpacked. It is important not to change the name of unpacked directory as it name should be
'*NKJP-PodkorpusMilionowy-1.2*'.

* In order to use python scripts available in this project without encountering any unnecessary difficulties it is implored 
not to change the original structure of the project.

* Some examples of using scripts with exemplary arguments:
 * **nkjp_parsing_and_serialization.py**:
   * If you downloaded and unpacked the 1-million-word subcorpus into resources directory of the project than you do not have 
     to specify the *NKJP_dir_path* argument. Just simply run script with following argument:  
     `python3 nkjp_parsing_and_serialization.py /home/kaspiotr/Dev/MorphosyntacticTagger/resources/nkjp_output`
   * If not, you will have to specify the *NKJP_dir_path* argument 
     otherwise *OSError: Contents of directory named NKJP-PodkorpusMilionowy-1.2 not found in the specified location.* wiil be
     thrown:  
     `python3 nkjp_parsing_and_serialization.py /home/kaspiotr/Dev/MorphosyntacticTagger/resources/nkjp_output -NKJP_dir_path=/home/kaspiotr/Documents/NKJP-PodkorpusMilionowy-1.2/`
   * You can also run this script providing only the name of the output file:  
     `python3 nkjp_parsing_and_serialization.py nkjp_output` and the output file *nkjp_output* will be save in the *resources* directory of this project 
 * **maca_output_parsing_and_serialization.py**:
   * If you downloaded and unpacked the 1-million-word subcorpus into resources directory of the project than you do not have 
     to specify the *NKJP_dir_path* argument. Just simply run script with following argument:  
     `python3 maca_output_parsing_and_serialization.py /home/kaspiotr/Dev/MorphosyntacticTagger/resources/maca_output /home/kaspiotr/Dev/MorphosyntacticTagger/resources/maca_output_serialized_from_nkjp -NKJP_file_path=/home/kaspiotr/Dev/MorphosyntacticTagger/resources/nkjp_output.jsonl`
   * If not, you will have to specify the *NKJP_dir_path* argument 
     otherwise *OSError: Contents of directory named NKJP-PodkorpusMilionowy-1.2 not found in the specified location.* will be
     thrown:  
     `python3 maca_output_parsing_and_serialization.py /home/kaspiotr/Dev/MorphosyntacticTagger/resources/maca_output /home/kaspiotr/Dev/MorphosyntacticTagger/resources/maca_output_serialized_from_nkjp -NKJP_file_path=/home/kaspiotr/Dev/MorphosyntacticTagger/resources/nkjp_output.jsonl -NKJP_dir_path=/home/kaspiotr/Dev/MorphosyntacticTagger/resources/NKJP-PodkorpusMilionowy-1.2/`
   * If you saved your output *.jsonl file produced by script *nkjp_parsing_and_serialization.py* into *resources* directory of this project and named it *nkjp_output* than you do not have to specify the *NKJP_file_path* argument. You can simply run this script like that:  
     `python3 maca_output_parsing_and_serialization.py /home/kaspiotr/Dev/MorphosyntacticTagger/resources/maca_output /home/kaspiotr/Dev/MorphosyntacticTagger/resources/maca_output_serialized_from_nkjp -NKJP_dir_path=/home/kaspiotr/Dev/MorphosyntacticTagger/resources/NKJP-PodkorpusMilionowy-1.2/`   
   * You can also run this script providing only the names of the output files and if you saved your output *.jsonl file produced by script *nkjp_parsing_and_serialization.py* into *resources* directory of this project and named it *nkjp_output* you can just write:  
     `python3 maca_output_parsing_and_serialization.py maca_output maca_output_serialized_from_nkjp` and the output files *maca_output* and *maca_output_serialized_from_nkjp* will be save in the *resources* directory of this project.
 * **maca_and_nkjp_output_merge.py**:
   * You can run this script providing as it's first argument the absolute path to the *.jsonl with marked similarities in POS tagging between MACA output and NKJP corpora:  
   `python3 maca_and_nkjp_output_merge.py /home/kaspiotr/Dev/MorphosyntacticTagger/output/maca_output_marked.jsonl -NKJP_file='/home/kaspiotr/Dev/MorphosyntacticTagger/resources/nkjp_output.jsonl' -MACA_file=/home/kaspiotr/Dev/MorphosyntacticTagger/resources/maca_output_serialized_from_nkjp.jsonl`
   * or you can run this script providing only the name of the output *.jsonl file and than it will be saved in the output directory of this project:  
   `python3 maca_and_nkjp_output_merge.py maca_output_marked.jsonl -NKJP_file=/home/kaspiotr/Dev/MorphosyntacticTagger/resources/nkjp_output.jsonl -MACA_file=/home/kaspiotr/Dev/MorphosyntacticTagger/resources/maca_output_serialized_from_nkjp.jsonl`
   * If you saved your output *.jsonl file produced by script *nkjp_parsing_and_serialization.py* into *resources* directory of this project and named it *nkjp_output* than you do not have to specify the *NKJP_file* argument. You can simply run this script like that:  
   `python3 maca_and_nkjp_output_merge.py maca_output_marked -MACA_file=/home/kaspiotr/Dev/MorphosyntacticTagger/resources/maca_output.jsonl` 
   * If you saved your output *.jsonl file produced by script *maca_output_parsing_and_serialization.py* into *resources* directory of this project and named it *maca_output_serialized_from_nkjp* than you do not have to specify the *MACA_file* argument. You can simply run this script like that:  
   `python3 maca_and_nkjp_output_merge.py maca_output_marked`  
   This script will create file *maca_output_marked* that will be saved in *resources/output* directory of this project.  
   This script will also log information included in provided as parameters *.jsonl files and log them into a file called tagging_diff.log
   that will be saved in resources directory of this project. File with logs will include such informations as:  
     * total number of paragraphs in NKJP corpora and constructed by MACA analyzer,  
     * total number of sentences in NKJP corpora and constructed by MACA analyzer,  
     * number of sentences that are tokenized in the same way by MACA analyzer as they are tokenized in NKJP corpora
   Additionally there was added is_test_mode_on argument to the script that allows, if set to True, to generate *maca_output_marked_test* file used 
   in tests. This argument is set to False by default.
 * **log_info_about_input_files_used_for_training.py**:  
 This script will create _maca_and_nkjp_tokens_merge_info.log_ file in output directory of this project with information following information from *maca_output_marked* file saved in the same directory:  
    - Total no. of MACA sentences: *81447*
    - No. of sentences with the same tokenization between the NKJP and the MACA: *79049*
    - No. of sentences with different tokenization between the NKJP and the MACA: *2398*
    - Total no. of MACA tokens: *1218612*
    - No. of MACA tokens with tag and base_form set from the NKJP corpora: *1205065*
    - No. of MACA tokens with 'ign' tag and base_form: *13547*
    - No. of MACA tokens with 'ign' tag and base_form set from the NKJP: *0*
    - No. of MACA tokens with 'ign' base_form and tag set from the NKJP: *0*
 * **training.py** (with use of the 1-million-word NCP subcorpus and stratified 10-fold cross validation method):
   * you can ran this script providing as it's first argument stratified 10 fold (SKF) cross validation split (from range 1 to 10) that you want to use for training the model and second argument with the name of *.jsonl file created by *maca_and_nkjp_output_merge.py* script.   
   If you didn't changed anything (renamed file *maca_output_marked* or moved it to another directory) this file should be called *maca_output_marked* and located in *output* directory of this project. In that case you can run script like that:  
   `python3 maca_and_nkjp_output_merge.py 1`  
   If you moved *maca_output_marked* to another directory (other that *output*) provide as a second argument of the script full path to that directory. Run script as follows:  
   `python3 maca_and_nkjp_output_merge.py 1 -file_path=/home/kaspiotr/Dev/MorphosyntacticTagger/output/maca_output_marked.jsonl`  
   If you left *maca_output_marked* in *output* directory of the project but renamed it provide the name of that *.jsonl file as a second argument of the script:  
   `python3 maca_and_nkjp_output_merge.py 1 -file_path=renamed_file_name`  
   This script will train models for given (as a parameter) SKF split number. Data needed to train models need to be saved in _data_ folder of this project. Models will be saved in _resources_ directory of this project.  
   If you want to train models for all 10 SKF splits on _Prometheus_ at once use one of the scripts provided:  
     - [train_on_K40XL.sh](https://github.com/kaspiotr/Morphosyntactic-tagger/blob/master/train_on_K40XL.sh)
     - [train_on_V100.sh](https://github.com/kaspiotr/Morphosyntactic-tagger/blob/master/train_on_V100.sh)
 * **convert_tsv_to_xml.py**:  
   This script converts *test.tsv* file that are generated for each stratified 10-fold cross validation split training to *test_n.xml* file (where *n* is the number of split). Files *test_n.xml* are used by [*tagger-eval.py*](https://github.com/kaspiotr/Morphosyntactic-tagger-evaluation/blob/master/tagger-eval.py) script to evaluate tagger. 
   Files *test_n.xml* are saved in _resources_ directory of this project.
 * **convert_nkjp_to_xml.py**:  
   This script generates *nkjp_ref_n* files for each stratified 10-fold cross validation split (where *n* is the number of split) corresponding to given *test_n.xml* file generated by **convert_tsv_to_xml.py** script. Files *nkjp_ref_n.xml* are used by [*tagger-eval.py*](https://github.com/kaspiotr/Morphosyntactic-tagger-evaluation/blob/master/tagger-eval.py) script to evaluate tagger.
   Files *nkjp_ref_n.xml* are saved in _resources_ directory of this project. To run this script you need to create a _nkjp_data_ directory in the main directory of this project.  
   This script could also be ran on _Prometheus_ with use of following script (it is essential to run it on the same host training was done due to get the same SKF split to this made during training of the model):
     - [convert_nkjp_to_xml.sh](https://github.com/kaspiotr/Morphosyntactic-tagger/blob/master/convert_nkjp_to_xml.sh) 
     
 #### Experiments (with use of the 1-million-word NCP subcorpus and stratified 10-fold cross validation method):  
 * Scripts that should be run before any of experiments before performing any of experiments mentioned after:  
   * **download_and_save_pl_fast_text_embeddings_model.py**:  
   It is recommended to run this script before training any model that uses Polish FastText WordEmbeddings (WordEmbeddings('pl') in its StackedEmbeddings configuration) in order to use embeddings that are stored locally
   instead of downloading them for each stratified k-fold cross validation split during model training.  
   This script could also be ran on _Prometheus_ with use of following script:
     - [download_and_save_pl_fast_text_embeddings_model.sh](https://github.com/kaspiotr/Morphosyntactic-tagger/blob/master/download_and_save_pl_fast_text_embeddings_model.sh)
   * **create_and_save_polish_letters_dictionary.py**:  
   If model use in its StackedEmbeddings configuration CharacterEmbeddings it is recommended to run the following script before training such a model in order to have every possible Polish letter in dictionary that they are using.  
   In order to do so on _Prometheus_ run following script:
     - [create_and_save_polish_letters_dictionary.sh](https://github.com/kaspiotr/Morphosyntactic-tagger/blob/master/create_and_save_polish_letters_dictionary.sh)  
 * First experiment:  
   * **training_without_backward_model.py**:      
   You can ran this script providing as it's first argument stratified 10 fold (SKF) cross validation split (from range 1 to 10) that you want to use for training the model and second argument with the name of *.jsonl file created by *maca_and_nkjp_output_merge.py* script.   
   If you didn't changed anything (renamed file *maca_output_marked* or moved it to another directory) this file should be called *maca_output_marked* and located in *output* directory of this project. In that case you can run script like that:  
   `python3 maca_and_nkjp_output_merge.py 1`  
   If you moved *maca_output_marked* to another directory (other that *output*) provide as a second argument of the script full path to that directory. Run script as follows:  
   `python3 maca_and_nkjp_output_merge.py 1 -file_path=/home/kaspiotr/Dev/MorphosyntacticTagger/output/maca_output_marked.jsonl`  
   If you left *maca_output_marked* in *output* directory of the project but renamed it provide the name of that *.jsonl file as a second argument of the script:  
   `python3 maca_and_nkjp_output_merge.py 1 -file_path=renamed_file_name`  
   This script will train models for given (as a parameter) SKF split number. This time backward model from _Flair_ will not be used in training. Data needed to train models need to be saved in _data_ex_1_ folder of this project. Models will be saved in _resources_ex_1_ directory of this project.  
   If you want to train models for all 10 SKF splits on Prometheus at once use one of the scripts provided:  
     - [train_on_K40XL_ex_1.sh](https://github.com/kaspiotr/Morphosyntactic-tagger/blob/master/train_on_K40XL_ex_1.sh)
     - [train_on_V100_ex_1.sh](https://github.com/kaspiotr/Morphosyntactic-tagger/blob/master/train_on_V100_ex_1.sh)  
   * **convert_tsv_to_xml_ex_1.py**:  
   This script converts *test.tsv* file that are generated for each stratified 10-fold cross validation split training to *test_n.xml* file (where *n* is the number of split). Files *test_n.xml* are used by [*tagger-eval.py*](https://github.com/kaspiotr/Morphosyntactic-tagger-evaluation/blob/master/tagger-eval.py) script to evaluate tagger. 
   Files *test_n.xml* are saved in _resources_ex_1_ directory of this project.  
 * Second experiment:  
   * **training_experiment_2.py**:  
   You can ran this script providing as it's first argument stratified 10 fold (SKF) cross validation split (from range 1 to 10) that you want to use for training the model and second argument with the name of *.jsonl file created by *maca_and_nkjp_output_merge.py* script.   
   If you didn't changed anything (renamed file *maca_output_marked* or moved it to another directory) this file should be called *maca_output_marked* and located in *output* directory of this project. In that case you can run script like that:  
   `python3 maca_and_nkjp_output_merge.py 1`  
   If you moved *maca_output_marked* to another directory (other that *output*) provide as a second argument of the script full path to that directory. Run script as follows:  
   `python3 maca_and_nkjp_output_merge.py 1 -file_path=/home/kaspiotr/Dev/MorphosyntacticTagger/output/maca_output_marked.jsonl`  
   If you left *maca_output_marked* in *output* directory of the project but renamed it provide the name of that *.jsonl file as a second argument of the script:  
   `python3 maca_and_nkjp_output_merge.py 1 -file_path=renamed_file_name`  
   This script will train models for given (as a parameter) SKF split number. This time only static WordEmbeddings trained over Polish Wikipedia and CharacterEmbeddings will be used in training. Data needed to train models need to be saved in _data_ex_2_ folder of this project. Models will be saved in _resources_ex_2_ directory of this project.  
   If you want to train models for all 10 SKF splits on Prometheus at once use one of the scripts provided:  
     - [train_on_K40XL_ex_2.sh](https://github.com/kaspiotr/Morphosyntactic-tagger/blob/master/train_on_K40XL_ex_2.sh)
     - [train_on_V100_ex_2.sh](https://github.com/kaspiotr/Morphosyntactic-tagger/blob/master/train_on_V100_ex_2.sh)
   * **convert_tsv_to_xml_ex_2.py**:  
   This script converts *test.tsv* file that are generated for each stratified 10-fold cross validation split training to *test_n.xml* file (where *n* is the number of split). Files *test_n.xml* are used by [*tagger-eval.py*](https://github.com/kaspiotr/Morphosyntactic-tagger-evaluation/blob/master/tagger-eval.py) script to evaluate tagger. 
   Files *test_n.xml* are saved in _resources_ex_2_ directory of this project.
 * Third experiment:  
   * **training_experiment_3.py**:  
   You can ran this script providing as it's first argument stratified 10 fold (SKF) cross validation split (from range 1 to 10) that you want to use for training the model and second argument with the name of *.jsonl file created by *maca_and_nkjp_output_merge.py* script.   
   If you didn't changed anything (renamed file *maca_output_marked* or moved it to another directory) this file should be called *maca_output_marked* and located in *output* directory of this project. In that case you can run script like that:  
   `python3 maca_and_nkjp_output_merge.py 1`  
   If you moved *maca_output_marked* to another directory (other that *output*) provide as a second argument of the script full path to that directory. Run script as follows:  
   `python3 maca_and_nkjp_output_merge.py 1 -file_path=/home/kaspiotr/Dev/MorphosyntacticTagger/output/maca_output_marked.jsonl`  
   If you left *maca_output_marked* in *output* directory of the project but renamed it provide the name of that *.jsonl file as a second argument of the script:  
   `python3 maca_and_nkjp_output_merge.py 1 -file_path=renamed_file_name`  
   This script will train models for given (as a parameter) SKF split number. This time only static WordEmbeddings trained over Polish Wikipedia, CharacterEmbeddings and OneHotEmbeddingsEmbeddings (to encode information about proposed tags for each token) will be used in training. Data needed to train models need to be saved in _data_ex_3_ folder of this project. Models will be saved in _resources_ex_3_ directory of this project.  
   If you want to train models for all 10 SKF splits on Prometheus at once use one of the scripts provided:  
     - [train_on_K40XL_ex_3.sh](https://github.com/kaspiotr/Morphosyntactic-tagger/blob/master/train_on_K40XL_ex_3.sh)
     - [train_on_V100_ex_3.sh](https://github.com/kaspiotr/Morphosyntactic-tagger/blob/master/train_on_V100_ex_3.sh)  
   * **convert_tsv_to_xml_ex_3.py**:  
   This script converts *test.tsv* file that are generated for each stratified 10-fold cross validation split training to *test_n.xml* file (where *n* is the number of split). Files *test_n.xml* are used by [*tagger-eval.py*](https://github.com/kaspiotr/Morphosyntactic-tagger-evaluation/blob/master/tagger-eval.py) script to evaluate tagger. 
   Files *test_n.xml* are saved in _resources_ex_3_ directory of this project.
 * Fourth experiment:  
   * **training_experiment_4.py**:  
   You can ran this script providing as it's first argument stratified 10 fold (SKF) cross validation split (from range 1 to 10) that you want to use for training the model and second argument with the name of *.jsonl file created by *maca_and_nkjp_output_merge.py* script.   
   If you didn't changed anything (renamed file *maca_output_marked* or moved it to another directory) this file should be called *maca_output_marked* and located in *output* directory of this project. In that case you can run script like that:  
   `python3 maca_and_nkjp_output_merge.py 1`  
   If you moved *maca_output_marked* to another directory (other that *output*) provide as a second argument of the script full path to that directory. Run script as follows:  
   `python3 maca_and_nkjp_output_merge.py 1 -file_path=/home/kaspiotr/Dev/MorphosyntacticTagger/output/maca_output_marked.jsonl`  
   If you left *maca_output_marked* in *output* directory of the project but renamed it provide the name of that *.jsonl file as a second argument of the script:  
   `python3 maca_and_nkjp_output_merge.py 1 -file_path=renamed_file_name`  
   This script will train models for given (as a parameter) SKF split number. This time model will be trained in with the same configuration as the basic one (trained with script **training.py**), where the number of RRN layers was set to 1 (rrn_layers=1 -default value for the parameter), but this time  
   trained model will have 2 RNN layers (parameter rnn_layers=2):
     - [train_on_K40XL_ex_4.sh](https://github.com/kaspiotr/Morphosyntactic-tagger/blob/master/train_on_K40XL_ex_4.sh)
     - [train_on_V100_ex_4.sh](https://github.com/kaspiotr/Morphosyntactic-tagger/blob/master/train_on_V100_ex_4.sh)  
   * **convert_tsv_to_xml_ex_4.py**:  
   This script converts *test.tsv* file that are generated for each stratified 10-fold cross validation split training to *test_n.xml* file (where *n* is the number of split). Files *test_n.xml* are used by [*tagger-eval.py*](https://github.com/kaspiotr/Morphosyntactic-tagger-evaluation/blob/master/tagger-eval.py) script to evaluate tagger. 
   Files *test_n.xml* are saved in _resources_ex_4_ directory of this project.  
 * Fifth experiment:  
   * **training_experiment_5.py**:  
   You can ran this script providing as it's first argument stratified 10 fold (SKF) cross validation split (from range 1 to 10) that you want to use for training the model and second argument with the name of *.jsonl file created by *maca_and_nkjp_output_merge.py* script.   
   If you didn't changed anything (renamed file *maca_output_marked* or moved it to another directory) this file should be called *maca_output_marked* and located in *output* directory of this project. In that case you can run script like that:  
   `python3 maca_and_nkjp_output_merge.py 1`  
   If you moved *maca_output_marked* to another directory (other that *output*) provide as a second argument of the script full path to that directory. Run script as follows:  
   `python3 maca_and_nkjp_output_merge.py 1 -file_path=/home/kaspiotr/Dev/MorphosyntacticTagger/output/maca_output_marked.jsonl`  
   If you left *maca_output_marked* in *output* directory of the project but renamed it provide the name of that *.jsonl file as a second argument of the script:  
   `python3 maca_and_nkjp_output_merge.py 1 -file_path=renamed_file_name`  
   This script will train models for given (as a parameter) SKF split number. This time model will be trained with the same configuration as the basic one (trained with script **training.py**), but this time  
   trained model will have also static WordEmbeddings (FastText embeddings trained over Polish Wikipedia) in its StackedEmbeddings configuration:
     - [train_on_K40XL_ex_5.sh](https://github.com/kaspiotr/Morphosyntactic-tagger/blob/master/train_on_K40XL_ex_5.sh)
     - [train_on_V100_ex_5.sh](https://github.com/kaspiotr/Morphosyntactic-tagger/blob/master/train_on_V100_ex_5.sh)  
   * **convert_tsv_to_xml_ex_5.py**:  
   This script converts *test.tsv* file that are generated for each stratified 10-fold cross validation split training to *test_n.xml* file (where *n* is the number of split). Files *test_n.xml* are used by [*tagger-eval.py*](https://github.com/kaspiotr/Morphosyntactic-tagger-evaluation/blob/master/tagger-eval.py) script to evaluate tagger. 
   Files *test_n.xml* are saved in _resources_ex_5_ directory of this project.    
 * Sixth experiment:  
   * **training_experiment_6.py**:  
   You can ran this script providing as it's first argument stratified 10 fold (SKF) cross validation split (from range 1 to 10) that you want to use for training the model and second argument with the name of *.jsonl file created by *maca_and_nkjp_output_merge.py* script.   
   If you didn't changed anything (renamed file *maca_output_marked* or moved it to another directory) this file should be called *maca_output_marked* and located in *output* directory of this project. In that case you can run script like that:  
   `python3 maca_and_nkjp_output_merge.py 1`  
   If you moved *maca_output_marked* to another directory (other that *output*) provide as a second argument of the script full path to that directory. Run script as follows:  
   `python3 maca_and_nkjp_output_merge.py 1 -file_path=/home/kaspiotr/Dev/MorphosyntacticTagger/output/maca_output_marked.jsonl`  
   If you left *maca_output_marked* in *output* directory of the project but renamed it provide the name of that *.jsonl file as a second argument of the script:  
   `python3 maca_and_nkjp_output_merge.py 1 -file_path=renamed_file_name`  
   This script will train models for given (as a parameter) SKF split number. This time model will be trained with the same configuration as the basic one (trained with script **training.py**), but this time  
   trained model will have also static WordEmbeddings (FastText embeddings trained over Polish Wikipedia) in its StackedEmbeddings configuration. Furthermore trained model will have 2 RNN layers (parameter rnn_layers=2):
     - [train_on_K40XL_ex_6.sh](https://github.com/kaspiotr/Morphosyntactic-tagger/blob/master/train_on_K40XL_ex_6.sh)
     - [train_on_V100_ex_6.sh](https://github.com/kaspiotr/Morphosyntactic-tagger/blob/master/train_on_V100_ex_6.sh)  
   * **convert_tsv_to_xml_ex_6.py**:  
   This script converts *test.tsv* file that are generated for each stratified 10-fold cross validation split training to *test_n.xml* file (where *n* is the number of split). Files *test_n.xml* are used by [*tagger-eval.py*](https://github.com/kaspiotr/Morphosyntactic-tagger-evaluation/blob/master/tagger-eval.py) script to evaluate tagger. 
   Files *test_n.xml* are saved in _resources_ex_6_ directory of this project.
   
 #### Training with use of the PolEval 2017 data:      
 Training morphosyntactic tagger model of Polish language based on contextual word embeddings that solves  
 **Task 1: POS Tagging - Subtask (A): Morphosyntactic disambiguation and guessing**  
 Task definition is available here: [Subtask (A): Morphosyntactic disambiguation and guessing](http://2017.poleval.pl/index.php/tasks/)  
 Training data used are available to download [here](http://2017.poleval.pl/index.php/tasks/):  
   - [train-analyzed.xml.gz](http://2017.poleval.pl/index.php/tasks/train-analyzed.xml.gz) (from this file tokens changed form, )
   - [train-gold.xml.gz](http://2017.poleval.pl/index.php/tasks/train-gold.xml.gz)
 Test data used are available to download [here](http://2017.poleval.pl/index.php/results/):  
   - [test-analyzed.xml.gz](http://2017.poleval.pl/index.php/tasks/train-gold.xml.gz)
   - [gold-task-a-b.xml.gz](http://2017.poleval.pl/index.php/results/gold-task-a-b.xml.gz)
 * **training_on_pol_eval_data.py**:  
 Script used to train tagger's model with the same configuration as the one trained in _Sixth_experiment_ described above. Before you ran this script you need to create directories called _data_pol_eval_ and _resources_pol_eval_ in the root  
 directory of this project. Then download to _resources_pol_eval_ directory following files:  
 _train-analyzed.xml_, _train-gold.xml_ and _test-analyzed.xml_ and _gold-task-a-b.xml files_.   
 After unzipping downloaded files just run script and you will perform training locally.   
 To train model on _Prometheus_ you can use following script:
   - [train_on_V100_pol_eval.sh](https://github.com/kaspiotr/Morphosyntactic-tagger/blob/master/train_on_V100_pol_eval.sh)  
 * **convert_tsv_to_xml_pol_eval.py**:  
   This script converts *test.tsv* file that are generated in model's training to *test.xml* file.  
   File *test.xml* is used by [*tagger-eval.py*](https://github.com/kaspiotr/Morphosyntactic-tagger-evaluation/blob/master/tagger-eval.py) script to evaluate tagger model. 