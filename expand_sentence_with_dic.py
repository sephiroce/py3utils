#-.*.- Encoding:utf-8 -.*.-
import sys

debug = False

if len(sys.argv) < 4:
    print("!!USAGE: ./expand_sentence_with_dic.py dict(sample: librispeech-lexicon.txt) src.txt dst.txt (optional)N")

N = 10
if len(sys.argv) == 5:
    N = int(sys.argv[4])

#Load dic
pron_dict=dict()
word_dict=dict()
with open(sys.argv[1]) as f:
    for line in f:
        #Word to Pron
        words = line.split()
        key = words[0]
        value = str( words[1:] ).replace( "['", "" ).replace( "']", "" ).replace( "', '", " " )

        # Word to Pron
        if key not in pron_dict:
            pron_dict[key] = list()
        pron_dict[key].append( value )

        #Pron to Word
        if value not in word_dict:
            word_dict[value] = list()
        word_dict[value].append( key )


num_of_value = 0
for key in pron_dict:
    num_of_value += len( pron_dict[key] )

print("INFO: %d vocabs, %d pronunciations were loaded." % (len( pron_dict ), num_of_value) )
line_trees = list()

dst_file = open(sys.argv[3],"w")

#TODO: It uses DFS, BFS could be better way to expand sentences?
def word2lex(sentence, line_array, idx, pseq_list):
    if len(pseq_list) >= N or idx >= len(line_array):
        return

    cur_word = line_array[idx]

    if len( line_array ) - 1 == idx:
        if cur_word in pron_dict:
            for pron in pron_dict[cur_word]:
                if len( pseq_list ) >= N:
                    return
                pseq_list.append( "%s P'%s'" % (sentence, pron) )
        else:
            if len( pseq_list ) >= N:
                return pseq_list
            pseq_list.append( "%s W'%s'" % (sentence, cur_word) )
            return

    if cur_word in pron_dict:
        for pron in pron_dict[cur_word]:
            word2lex ("%s P'%s'" % (sentence, pron), line_array, idx + 1, pseq_list)
    else:
        word2lex( "%s W'%s'" % (sentence, cur_word), line_array, idx + 1, pseq_list)
    return

def lex2word(sentence, line_array, idx, wseqs):
    if len( wseqs ) >= N or idx >= len( line_array ):
        return

    cur_word = line_array[idx]

    if len( line_array ) - 1 == idx:
        if cur_word.startswith("P"):
            for pron in word_dict[cur_word[2:]]:
                if len( wseqs ) >= N:
                    return
                wseqs.add( "%s %s" % (sentence, pron) )
        else:
            if len( wseqs ) >= N:
                return wseqs
            wseqs.add( "%s %s" % (sentence, cur_word[2:-1]) )
            return

    if cur_word.startswith( "P" ):
        for pron in word_dict[cur_word[2:]]:
            lex2word ("%s %s" %(sentence, pron), line_array, idx + 1, wseqs )
    else:
        lex2word( "%s %s" %(sentence, cur_word[2:]), line_array, idx + 1, wseqs )
    return

with open(sys.argv[2]) as f:
    for line in f:
        pseq_list = list()
        wseq_set = set()
        if debug:
            print( "An original word sequence:" )
            print(line.strip())
        # Word to Pron :
        # -> input : line
        # -> output: pseq_list
        sid = int(line.split()[0])
        word2lex( "", line.split(), 1, pseq_list )

        if debug:
            print("Phone sequences:")
            for idx, pline in enumerate(pseq_list,start = 1):
                print("%d-%d %s"%(sid,idx,pline.strip()))

        # Pron to Word
        # -> input : pseq_list
        # -> output: wseq_list
        last_pid = 0
        for pid, pline in enumerate( pseq_list, start=1 ):
            wseqs = set()
            lex2word( "", pline[:-1].strip().split("' "), 0, wseqs )
            for wseq in wseqs:
                if len( wseq_set ) >= N:
                    break
                if wseq == line.strip():
                    continue
                wseq_set.add( wseq )
                last_pid = pid

        if debug:
            print( "Expanded word sequences:" )
            for idx, wline in enumerate(wseq_set,start = 1):
                print("%d-%d %s"%(sid,idx,wline.strip()))
