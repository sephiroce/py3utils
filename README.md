# py3util
Python3 utility scripts especially for someone who researches automatic speech recognition and language modelling.

## Identically pronounced sentence generator
This script generates several word sequences which have same pronunciation.
I used librispeech(http://www.openslr.org/11/) as sample data.   

### USAGE
```$python3 expand_sentence_with_dic.py dict(sample: librispeech-lexicon.txt) src.txt (optional)N```

!! BEWARE  
This script is in an alpha version and it is just verified to generate intended word sequences.

### Input
src.txt should be contains Sequence ID at the beginning of sentences.
ex)
```
900 A B I SHE HATH THIS MOMENT CONFESSED IT
901 A B I SHE REFUSETH TO COME
902 A B I THOU KNOWEST MEN MISTRESS
903 A B I WITH HER THERE IS NO JESTING
904 A B INFORMATION WANTED CONCERNING
...
```
You can use sequence ID for mapping original sequences to the expanded sequences.

### Output
The outputs of the 900th sentence.
```
900-1 A B AI SHE HATH THIS' MOMENT CONFESSED IT
900-2 A B AI SHE HATH THIS' MOMENT CONFEST IT
900-3 A B AI SHE HATH THIS MOMENT CONFEST IT
900-4 A B AI SHE' HATH THIS' MOMENT CONFESSED IT
900-5 A B AI SHE HATH THIS MOMENT CONFESSED IT
900-6 A B AI SHE' HATH THIS' MOMENT CONFEST IT
900-7 A B AI SHE'L HATH THIS MOMENT CONFESSED IT
900-8 A B AI SHE'L HATH THIS MOMENT CONFEST IT
900-9 A B AI SHE' HATH THIS MOMENT CONFESSED IT
900-10 A B AI SHE' HATH THIS MOMENT CONFEST IT
```