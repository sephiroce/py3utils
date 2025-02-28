# py3util
Python3 utility scripts especially for someone who researches automatic speech recognition and language modelling.

## extract_words.py: get words from text corpus
This script extract words from text corpus without duplication.

## Pre-requsite
- Please put the latest kaldi (8th-Feb-2019) in tools

### USAGE
```
	python3 extract_words.py in:text_corpus
```

### TO-DO
- adding an option for allowing duplication
- adding an option for counting the number of each word

## chk_filelist.py: file checker
This script checks whether files in the given list exist or not.

### USAGE
```
	python3 chk_filelist.py list_of_files
```

## expand_sentence_with_dic.py: Identically pronounced sentence generator
This script generates several word sequences which have same pronunciation.
I used librispeech(http://www.openslr.org/11/) as sample data.   

### USAGE
```
  python3 expand_sentence_with_dic.py w/ options listed up below.
  
  required)
  --eswd-lex ESWD_LEX, --lex ESWD_LEX
                        lexicon.
  --eswd-text ESWD_TEXT, --text ESWD_TEXT
                        text corpus to be expanded.
  
  optional)             
  --eswd-save-sid-corpus ESWD_SAVE_SID_CORPUS, --sid-corpus ESWD_SAVE_SID_CORPUS
                        Whether saving text corpus including sequential id or not. (default = True)
  --eswd-max-expanded-sentence ESWD_MAX_EXPANDED_SENTENCE, --max-n ESWD_MAX_EXPANDED_SENTENCE
                        The maximum number of expanded sentences for each sentence.
  --eswd-min-sentence-levenshtein-distance-rate ESWD_MIN_SENTENCE_LEVENSHTEIN_DISTANCE_RATE, --min-lev-rate ESWD_MIN_SENTENCE_LEVENSHTEIN_DISTANCE_RATE
                        min levenshtein distance between reference sentence and expanded sentences.
  --eswd-min-sentence-levenshtein-distance ESWD_MIN_SENTENCE_LEVENSHTEIN_DISTANCE, --min-lev ESWD_MIN_SENTENCE_LEVENSHTEIN_DISTANCE
                        min levenshtein distance between reference sentence and expanded sentences.                     
```                        

### Input
#### Lexicon: eswd-lex
ex) samples/librispeech-lexicon.txt  
word[TAB]phone
```
A'BODY  EY1 B AA2 D IY0
A'COURT EY1 K AO2 R T
```
#### Text corpus: eswd-text
ex) samples/test.100.txt
```
A B I SHE HATH THIS MOMENT CONFESSED IT
A B I SHE REFUSETH TO COME
...
```

### Output
#### (optional) Sequential id corpus: ${eswd-text}.sid
ex) samples/test.100.txt.sid
sid[blank]word sequence
```
1 A B I SHE HATH THIS MOMENT CONFESSED IT
2 A B I SHE REFUSETH TO COME
```
#### Expanded corpus: ${eswd-text}.exp
ex) samples/test.100.txt.exp
sid[blank]word sequence  
```
2 A B AI' SHIH REFUSETH TO COME
2 A B AIE SHE' REFUSETH TO CUM
2 A B AI SHE'L REFUSETH TOO COME
```
** The sequential ids can be used as mapping ids between original sentences and expanded sentences.
