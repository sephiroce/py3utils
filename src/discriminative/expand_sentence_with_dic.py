# -.*.- Encoding:utf-8 -.*.-

import sys
from common import Logger
from common import ParseOption
from levenshtein import levenshtein as lev
"""
word[tab]phone_sequence

example of lexicon

A  AH0
A  EY1
A''S    EY1 Z
A'BODY  EY1 B AA2 D IY0
A'COURT EY1 K AO2 R T
A'D     EY1 D
A'GHA   EY1 G AH0
A'GOIN  EY1 G OY1 N
A'LL    EY1 L
A'M     EY1 M
"""


# Load dic
class PhoneticCorpusExpander:
    def __init__(self, logger, config):
        self._logger = logger
        self._pron_dict = dict()
        self._word_dict = dict()
        self._config = config

        with open(config.eswd_lex) as lex_file:
            for lex_line in lex_file:
                # Word to Pron
                words = lex_line.split()
                key = words[0]
                value = str(words[1:]).replace("['", "").replace("']", "").replace("', '", " ")

                # Word to Pron
                if key not in self._pron_dict:
                    self._pron_dict[key] = list()
                self._pron_dict[key].append(value)

                # Pron to Word
                if value not in self._word_dict:
                    self._word_dict[value] = list()
                self._word_dict[value].append(key)

        num_of_value = 0
        for key in self._pron_dict:
            num_of_value += len(self._pron_dict[key])

        self._logger.info("%d vocabs, %d pronunciations were loaded." % (len(self._pron_dict), num_of_value))

    def _word2lex(self, sentence, line_array, word_idx, pseq_list):
        """
        This is a recursive method to find phone sequences of the given word sequence.
        :visibility: Private
        :param sentence:
        :param line_array:
        :param word_idx:
        :param pseq_list: phone level sequence
        :return: None
        """
        if len(pseq_list) >= self._config.eswd_max_expanded_sentence or word_idx >= len(line_array):
            return

        cur_word = line_array[word_idx]

        if len(line_array) - 1 == word_idx:
            if cur_word in self._pron_dict:
                for pron in self._pron_dict[cur_word]:
                    if len(pseq_list) >= self._config.eswd_max_expanded_sentence:
                        return
                    pseq_list.append("%s P'%s'" % (sentence, pron))
            else:
                if len(pseq_list) >= self._config.eswd_max_expanded_sentence:
                    return pseq_list
                pseq_list.append("%s W'%s'" % (sentence, cur_word))
                return

        if cur_word in self._pron_dict:
            for pron in self._pron_dict[cur_word]:
                self._word2lex("%s P'%s'" % (sentence, pron), line_array, word_idx + 1, pseq_list)
        else:
            self._word2lex("%s W'%s'" % (sentence, cur_word), line_array, word_idx + 1, pseq_list)
        return

    def _lex2word(self, sentence, line_array, idx, wseqs):
        """
        This is a recursive method to find word sequence of the given phone sequence.
        :param line_array:
        :param idx:
        :param wseqs:
        :return:
        """
        if len(wseqs) >= self._config.eswd_max_expanded_sentence or idx >= len(line_array):
            return

        cur_word = line_array[idx]

        if len(line_array) - 1 == idx:
            if cur_word.startswith("P"):
                for pron in self._word_dict[cur_word[2:]]:
                    if len(wseqs) >= self._config.eswd_max_expanded_sentence:
                        return
                    wseqs.add("%s %s" % (sentence, pron))
            elif cur_word.startswith("W"):
                if len(wseqs) >= self._config.eswd_max_expanded_sentence:
                    return wseqs
                wseqs.add("%s %s" % (sentence, cur_word[2:-1]))
                return
            else:
                self._logger.critical("The type of element must be either P or W, but %s.", cur_word[0])

        if cur_word.startswith("P"):
            for pron in self._word_dict[cur_word[2:]]:
                self._lex2word("%s %s" % (sentence, pron), line_array, idx + 1, wseqs)
        elif cur_word.startswith("W"):
            self._lex2word("%s %s" % (sentence, cur_word[2:]), line_array, idx + 1, wseqs)
        else:
            self._logger.critical("The type of element must be either P or W, but %s.", cur_word[0])
        return

    def expand_corpus(self):
        sid = 0
        f_text = open(self._config.eswd_text)
        w_text = open(
            "%s.%dto%d.exp" % (self._config.eswd_text, self._config.eswd_sid_start, self._config.eswd_sid_end), "w" )
        sf_text = None
        if self._config.eswd_save_sid_corpus:
            sf_text = open(
                "%s.%dto%d.sid" % (self._config.eswd_text, self._config.eswd_sid_start, self._config.eswd_sid_end),
                "w" )

        expd_line_n = 0
        zero_line_n = 0

        line_n = 0
        for line in f_text:
            sid += 1
            if sid > self._config.eswd_sid_end > -1:
                break
            if sid < self._config.eswd_sid_start:
                continue
            line_n+=1
            pseq_list = list()
            wseq_set = set()
            word_n = len(line.split())
            self._logger.debug("An original word sequence: %s" % line.strip())

            if sf_text is not None:
                sf_text.write("%d %s\n" % (sid, line.strip()))

            # Word to Pron :
            # -> input : line
            # -> output: pseq_list
            self._word2lex("", line.split(), 0, pseq_list)

            self._logger.debug("Phone sequences:")
            for idx, pline in enumerate(pseq_list, start=1):
                self._logger.debug("%d-%d %s" % (sid, idx, pline.strip()))

            # Pron to Word
            # -> input : pseq_list
            # -> output: wseq_list
            for pid, pline in enumerate(pseq_list, start=1):
                wseqs = set()
                self._lex2word("", pline[:-1].strip().split("' "), 0, wseqs)
                for wseq in wseqs:
                    if len(wseq_set) >= self._config.eswd_max_expanded_sentence:
                        break
                    if wseq == line.strip():
                        continue
                    lev_d = lev(wseq.split(), line.split())
                    lev_r = lev_d / word_n
                    if self._config.eswd_min_sentence_levenshtein_distance <= lev_d and \
                            self._config.eswd_min_sentence_levenshtein_distance_rate <= lev_r:
                            wseq_set.add(wseq)

            if len(wseq_set) == 0:
                self._logger.info("Zero line(sid: %d): %s" % (sid, line.strip()))
                zero_line_n += 1
            else:
                self._logger.debug("Expanded word sequences:")
                for idx, wline in enumerate(wseq_set, start=1):
                    lev_d = lev(wline.split(), line.split())
                    self._logger.debug("%d-%d %s, lev = %d" % (sid, idx, wline.strip(), lev_d))
                    w_text.write("%d %s\n" % (sid, wline.strip()))
                    expd_line_n += 1

        self._logger.info("Input lines: %d, expanded lines: %d, zero lines: %d" % (line_n, expd_line_n, zero_line_n))


def main():
    logger = Logger(name="KMPY3_UTILITY", level=Logger.INFO).logger
    po = ParseOption(sys.argv, logger)
    pce = PhoneticCorpusExpander(logger=logger, config=po.args)
    pce.expand_corpus()


if __name__ == "__main__":
    main()
