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
 * **maca_output_parsing_and_serialization.py**:
   * If you downloaded and unpacked the 1-million-word subcorpus into resources directory of the project than you do not have 
     to specify the *NKJP_dir_path* argument. Just simply run script with following argument:
     `python3 maca_output_parsing_and_serialization.py /home/kaspiotr/Dev/MorphosyntacticTagger/resources/nkjp_output.jsonl /home/kaspiotr/Dev/MorphosyntacticTagger/resources/maca_output /home/kaspiotr/Dev/MorphosyntacticTagger/resources/maca_output_serialized_from_nkjp`
   * If not, you will have to specify the *NKJP_dir_path* argument 
     otherwise *OSError: Contents of directory named NKJP-PodkorpusMilionowy-1.2 not found in the specified location.* wiil be
     thrown:  
     `python3 maca_output_parsing_and_serialization.py /home/kaspiotr/Dev/MorphosyntacticTagger/resources/nkjp_output.jsonl /home/kaspiotr/Dev/MorphosyntacticTagger/resources/maca_output /home/kaspiotr/Dev/MorphosyntacticTagger/resources/maca_output_serialized_from_nkjp -NKJP_dir_path=/home/kaspiotr/Dev/MorphosyntacticTagger/resources/NKJP-PodkorpusMilionowy-1.2/`
 * **maca_and_nkjp_output_merge.py**:
   `python3 maca_and_nkjp_output_merge.py /home/kaspiotr/Dev/MorphosyntacticTagger/resources/nkjp_output.jsonl /home/kaspiotr/Dev/MorphosyntacticTagger/resources/maca_output.jsonl /home/kaspiotr/Dev/MorphosyntacticTagger/resources/maca_output_marked.jsonl`
   
