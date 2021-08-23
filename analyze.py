import gzip, sys
from collections import Counter

def open_f(file):
    if file.endswith("gz"):
        fl = gzip.open(file, "rt")
    else:
        fl = open(file, "r")
    return(fl)

def count_words(data):
    count = 0 # this counter will count the words
    fl = open_f(data)
    for line in fl:
        line=line.strip() # clean
        if line and line[0].isdigit(): # skip metadata
#            print("counted", line) # if you want to see what we are counting, uncomment this
            count +=1
        else:
            continue
    return count

def most_frequent(data, col, how_many,*focus):
    cols = ["ID","FORM","LEMMA","UPOS","XPOS","FEAT","HEAD","DEPREL","DEPS","MISC"] #the columns of the conllu format
    my_counter = Counter()
    result = "" # here is where we put the result
    fl = open_f(data)
    for line in fl:
        line=line.strip()
        if not line or not line[0].isdigit(): # skip metadata and empty lines
                continue
        else:
                line=line.split("\t") # split to list
                if line[cols.index("UPOS")] == "PUNCT": # let's ignore punctuation
                        continue
                elif len(focus) == 0: # if 0, we take all, except for punctuation
                    my_counter[line[cols.index(col)]] +=1
                elif line[cols.index(col)] == "".join(focus): #if focus specifies a group we want to focus on, it is defined here
                         my_counter[line[2]] +=1 #take lemmas
    for word, count in my_counter.most_common(how_many):
        result = result + word + " " + str(count) + "\n"
    return(result)

def read_text(inp):
    id = None
    text = []
    for line in inp:
            line=line.strip()
            if line.startswith("# <doc id"):
                if id != None:
                    yield(register, text)
                    text = []
                    register = None
                    id = line
                elif id == None:
                    id=line
            elif line.startswith("# predicted register"):
                        register=line.split(":")[1].strip()
            elif not line.startswith("#"):
                if len(line)== 0:
                    continue
                else:
                    text.append(line.split("\t"))
            else:
                continue
    yield(register, text)

def extract_register(register, data):
    file_out = open(register + "_ext" + ".conllu", "w")
    for reg, text  in read_text(open_f(data)):
        if reg == register :
            file_out.write("# predicted register: " + register + "\n")
            for line in text:
                if line[0] == "1":
                    file_out.write("\n")
                file_out.write("\t".join(line)+"\n")
            file_out.write("\n")
    file_out.close()
    print("Wrote", register, "texts to a file!")
    return(file_out)


def print_text(data, col, max):
    cols = ["ID","FORM","LEMMA","UPOS","XPOS","FEAT","HEAD","DEPREL","DEPS","MISC"] #the columns of the conllu format
    to_return = []
    text_count = 0
    for reg, text in read_text(open_f(data)):
        text_count +=1
        if text_count > max:
            break
        else:
            words = (word_line[cols.index(col)] for word_line in text)
            to_return.append(" ".join(words))
    return("\n\n".join(to_return))


def count_specific_lemma(word, data, col):
    cols = ["ID","FORM","LEMMA","UPOS","XPOS","FEAT","HEAD","DEPREL","DEPS","MISC"]
    data=open_f(data)
    counter = 0
    result = ""
    myc = Counter()
    for line in data:
        if not line or not line[0].isdigit(): # skip metadata and empty lines
                continue
        else:
            line=line.strip().split("\t")
            if line[2] == word:
                    counter +=1
                    myc[line[cols.index(col)]] +=1
            else:
                    continue
    for w, count in myc.most_common(15):
        result = result + w + " " + str(count) + "\n"
    return("Total counts for the lemma " + word + ": " + str(counter)+"\n" + "The most frequent " + " " +  col + ":" + "\n" +result)

#print(count_specific_lemma("koira", sys.argv[1], "DEPREL"))

def count_word_context(word, column, data):
    data=open_f(data)
    before_window = []
    final_win = []
    after_counter = 0
    result = ""
    cols = ["ID","FORM","LEMMA","UPOS","XPOS","FEAT","HEAD","DEPREL","DEPS","MISC"] 
    for line in data:
        line=line.strip().split("\t")
        if not line or not line[0].isdigit(): # skip metadata and empty lines
            continue
        elif line[3] == "PUNCT":
            continue
        else:
            after_counter +=1
            before_window.append(line[cols.index(column)])
            if after_counter <=3:
                if len(final_win) >= 3:
                    final_win.append(line[cols.index(column)])
            elif line[1] == word:
                before_window.remove(line[cols.index(column)])
                final_win= final_win + before_window[-3:]
                before_window = []
                after_counter = 0
            else:
                continue
    for w, c in Counter(final_win).most_common(20):
        result = result + w + " " + str(c) + "\n"
    return(result)

#print(count_word_context("koira", "UPOS", sys.argv[1]))

# what are the most frequent tags (column, eg lemmas) for the searched_deprel?
def count_deprel(column, searched_deprel, data):#, col):
    cols = ["ID","FORM","LEMMA","UPOS","XPOS","FEAT","HEAD","DEPREL","DEPS","MISC"]
    data=open_f(data)
    counter = 0
    result = ""
    myc = Counter()
    for line in data:
        if not line or not line[0].isdigit(): # skip metadata and empty lines
                continue
        else:
            line=line.strip().split("\t")
            if line[cols.index("DEPREL")] == searched_deprel:
                    counter +=1
                    myc[line[cols.index(column)]] +=1
            else:
                    continue
    for w, count in myc.most_common(20):
        result = result + w + " " + str(count) + "\n"
    return("Total counts for the the dependency relation "  + searched_deprel + ": " + str(counter)+"\n" + "The most frequent " + " " +  column + ":" + "\n" +result)



#print(count_deprel("LEMMA", "nsubj", sys.argv[1])) 
