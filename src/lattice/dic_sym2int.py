import sys

def LoadDict(vocab_path, modify_quotation=False):
    if len(vocab_path ) > 0:
        vocab = dict()
        is_subword_nmt = False
        is_first_line = True
        with open(vocab_path) as f:
            for line_no, line in enumerate(f):
                w = line.strip()
                if line_no == 0 and w == "{":
                    is_subword_nmt = True
                    continue

                if is_subword_nmt:
                    if w == "}":
                        break
                    else:
                        p=w.split(": ")
                        v=p[0][1:len(p[0])-1]
                        i=int(p[1][0:len(p[1])-1])
                        if v == "<s>":
                            continue
                        else:
                            if modify_quotation and "\'" in v : 
                                v = "\"%s\""%v.replace("'","")
                            if i == 0 and v != "<eps>":
                                padding_eps = True
                                vocab["<eps>"] = i
                                print("%s doens't have <eps> thus <eps> is padded to 0"%vocab_path)
                            if padding_eps:
                                vocab[v] = i + 1 
                            else:
                                vocab[v] = i 
                else:
                    part = w.split("\t")[0].split(" ")[0]
                    if modify_quotation and "\'" in part :
                        part = "\"%s\""%part.replace("'","")
                    if line_no == 0 and part != "<eps>":
                        padding_eps = True
                        print("%s doens't have <eps> thus <eps> is padded to 0"%vocab_path)
                        vocab["<eps>"] = line_no

                    if padding_eps:
                        vocab[part] = line_no + 1 
                    else:
                        vocab[part] = line_no
        print("%d vocabs were loaded"%len(vocab))
        return vocab

if len(sys.argv) != 4:
    print("!!Usage: python3 dic_sym2int.py [dic] [phones-syms-table] [word-syms-table]")
    sys.exit(1)

phone_syms = LoadDict(sys.argv[2], True)
words_syms = LoadDict(sys.argv[3])

dic_int = open("%s.int"%sys.argv[1], "w")
dic_line = 0
with open(sys.argv[1]) as dic_file:
    for line in dic_file:
        dic_line += 1
        line = line.strip()
        part = line.split("\t")
        if len(part) != 2:
            print("Format error!")
            sys.exit(3)
        
        words_part = part[0].split(" ")
        phone_part = part[1].split(" ")

        words_idx = ""
        for word in words_part:
            if word not in words_syms:
                print("[%s] is not in loaded words"%word)
                sys.exit(2)
            words_idx += "%d"%words_syms[word] + " "
        
        phone_idx = ""
        for phon in phone_part:
            if phon not in phone_syms:
                if "\"" in phon:
                    phon = "'%s"%phon.replace("\"","")
                    if phon not in phone_syms:
                        print("%s is not in loaded phones"%phon)
                        sys.exit(2)
                else:
                    print("%s is not in loaded phones"%phon)
                    sys.exit(2)
            phone_idx += "%d"%phone_syms[phon] + " "

        dic_int.write("%s\t%s\n"%(words_idx.strip(), phone_idx.strip()))
print("Total %d lexicons were converted to int and saved to %s"%(dic_line, "%s.int"%sys.argv[1]))
