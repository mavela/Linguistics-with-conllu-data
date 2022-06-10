import sklearn.feature_extraction
from sklearn.svm import SVC
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import precision_score, recall_score, f1_score
import sys
from sklearn.metrics import classification_report
import re

labels_train=[]
labels_test=[]

feats_train=[]
feats_test=[]

def read_file(file):
    f_op = open(file,"r")
    labels = []
    feats = []
    for line in f_op:
        line=line.strip().split("\t")
        if len(line) == 1:
            continue
        else:
            feats.append(line[1])
            labels.append(line[0])
    return(labels,feats)
        
labels_train,feats_train = read_file(sys.argv[1])
labels_test,feats_test = read_file(sys.argv[2])

def data_iterator(f):
    for token in f:
        yield token


def tokenizer(txt):
    """Simple whitespace tokenizer"""
    return txt.split()


iterator=data_iterator(feats_train)
test_iterator=data_iterator(feats_test)
vectorizer=sklearn.feature_extraction.text.TfidfVectorizer(tokenizer=tokenizer,use_idf=True,min_df=0.005)
d=vectorizer.fit_transform(iterator)

d_test=vectorizer.transform(test_iterator)

classifier=SVC(C=0.5,kernel='linear',shrinking=False)
classifier.fit(d,labels_train)
labels_test_pred = classifier.predict(d_test)
print(classification_report(labels_test, labels_test_pred))


dens = classifier.coef_[0].todense()
densli = dens.tolist()
flat = []
for e in densli:
            flat.extend(e)

f_names=vectorizer.get_feature_names()
    
sorted_by_weight=sorted(zip(flat,f_names))
words = re.compile(r'^[a-zöäåA-ZÖÄÅ]+$')

print("Positive features for the first class")
for f_weight,f_name in sorted_by_weight[:30]:
    
            if re.search(words,f_name) != None:
                print(f_name)
 #           print("match", words.match(f_name))
print()
print("Positive features for the second class")
for f_weight,f_name in sorted_by_weight[-40:]:
     if re.search(words,f_name) != None:
            print(f_name)
