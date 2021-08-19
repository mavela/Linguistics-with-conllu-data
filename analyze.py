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

#print(most_frequent(sys.argv[1], "LEMMA", 10))

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
                    print("\n")
                    file_out.write("\n")
                file_out.write("\t".join(line)+"\n")
            file_out.write("\n")
    file_out.close()
    print("Wrote", register, "texts to a file!")
    return(file_out)

extract_register("narrative", sys.argv[1])
def print_text(data, col):
    cols = ["ID","FORM","LEMMA","UPOS","XPOS","FEAT","HEAD","DEPREL","DEPS","MISC"] #the columns of the conllu format
    to_return = []
    for reg, text in read_text(open_f(data)):
            words = (word_line[cols.index(col)] for word_line in text)
            print(" ".join(words))
    return(to_return)


        
