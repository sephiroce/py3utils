class VocabSymbolTable:
    @classmethod
    def LoadVocab(vocab_path):
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
                            vocab[i] = v
                else:
                    part = w.split("\t")[0].split(" ")[0]
                    vocab[line_no] = part
        print("%d vocabs were loaded"%len(vocab))
        return vocab

    @classmethod     
    def LoadDict(vocab_path, modify_quotation=False):
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
                            if padding_eps:
                                vocab[v] = i + 1
                            else:
                                vocab[v] = i
                else:
                    part = w.split("\t")[0].split(" ")[0]
                    if modify_quotation and "\'" in part :
                        part = "\"%s\""%part.replace("'","")
                    if line_no == 0 and v != "<eps>":
                        padding_eps = True
                        vocab["<eps>"] = line_no

                    if padding_eps:
                        vocab[part] = line_no + 1
                    else:
                        vocab[part] = line_no
        print("%d vocabs were loaded"%len(vocab))
        return vocab
