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
   `python3 maca_and_nkjp_output_merge.py /home/kaspiotr/Dev/MorphosyntacticTagger/output/maca_output_marked.jsonl -NKJP_file='/home/kaspiotr/Dev/MorphosyntacticTagger/resources/nkjp_output.jsonl' -MACA_file=/home/kaspiotr/Dev/MorphosyntacticTagger/resources/maca_output.jsonl`
   * or you can run this script providing only the name of the output *.jsonl file and than it will be saved in the output directory of this project:
   `python3 maca_and_nkjp_output_merge.py maca_output_marked.jsonl -NKJP_file='/home/kaspiotr/Dev/MorphosyntacticTagger/resources/nkjp_output.jsonl' -MACA_file=/home/kaspiotr/Dev/MorphosyntacticTagger/resources/maca_output.jsonl`
   * If you saved your output *.jsonl file produced by script *nkjp_parsing_and_serialization.py* into *resources* directory of this project and named it *nkjp_output* than you do not have to specify the *NKJP_file* argument. You can simply run this script like that:
   `python3 maca_and_nkjp_output_merge.py maca_output_marked -MACA_file=/home/kaspiotr/Dev/MorphosyntacticTagger/resources/maca_output.jsonl` 
   * If you saved your output *.jsonl file produced by script *maca_output_parsing_and_serialization.py* into *resources* directory of this project and named it *maca_output* than you do not have to specify the *MACA_file* argument. You can simply run this script like that:
   `python3 maca_and_nkjp_output_merge.py maca_output_marked`