
import pandas as pd
import pickle
import nltk
import re

nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from sklearn.feature_extraction.text import CountVectorizer

# Loading the dataset
df = pd.read_csv('Spam SMS Collection', sep='\t', names=['label', 'message'])
corpus = []
ps = PorterStemmer()

for i in range(0, df.shape[0]):
   
    message = re.sub(pattern='[^a-zA-Z]', repl=' ', string=df.message[i])

    
    message = message.lower()

   
    words = message.split()

   
    words = [word for word in words if word not in set(stopwords.words('english'))]

   
    words = [ps.stem(word) for word in words]

   
    message = ' '.join(words)

    
    corpus.append(message)




cv = CountVectorizer()
X = cv.fit_transform(corpus).toarray()


y = pd.get_dummies(df['label'])
y = y.iloc[:, 1].values


pickle.dump(cv, open('cv-transform.pkl', 'wb'))


from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)


from sklearn.naive_bayes import MultinomialNB

classifier = MultinomialNB(alpha=0.3)
classifier.fit(X_train, y_train)
pred=classifier.predict(X_test)

from sklearn.metrics import r2_score
print(r2_score(y_test, pred))


from sklearn.metrics import classification_report,confusion_matrix

print(confusion_matrix(y_test,pred))
print(classification_report(y_test,pred))

filename = 'spam-sms-mnb-model.pkl'
pickle.dump(classifier, open(filename, 'wb'))
