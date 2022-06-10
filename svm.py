import sklearn.feature_extraction
from sklearn.svm import SVC
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import precision_score, recall_score, f1_score
import sys
from sklearn.metrics import classification_report

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

