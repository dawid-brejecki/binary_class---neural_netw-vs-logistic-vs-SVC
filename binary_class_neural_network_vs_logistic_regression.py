# -*- coding: utf-8 -*-
"""binary_class - neural network vs logistic regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Wa4YiI0ZUR4IEkPyn05bo9HxtS8MyynJ
"""

import numpy as np
import pandas as pd
from keras.utils.np_utils import to_categorical 
from keras import models
from keras import layers
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from keras.utils.vis_utils import model_to_dot
from IPython.display import SVG
import matplotlib.pyplot as plt
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras import regularizers
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from mlxtend.plotting import plot_confusion_matrix
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

# ładowanie danych
df = pd.read_csv('credit.csv')
df.info()
df.describe()
df.isnull().sum()

# preprocessing
target = df.pop('default')

column_names_to_one_hot = ['SEX', 'EDUCATION', 'MARRIAGE', 'PAY_1', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5','PAY_6']

enc = OneHotEncoder()

enc_df = pd.DataFrame(enc.fit_transform(df[column_names_to_one_hot]).toarray())
df = df.join(enc_df)
df.drop(column_names_to_one_hot, axis=1, inplace=True)

X_train, X_test, Y_train, Y_test = train_test_split(df, target, test_size=0.25)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

shape = df.shape
  
# Printing Number of columns
print('Number of columns :', shape[1])

# budowanie modelu
network = models.Sequential()
# Dodanie warstwy wejsciowej z funkcją aktywacji ReLU
network.add(layers.Dense(units=91, activation='relu', input_shape=(91,)))
# Dodanie warstwy ukrytej z funkcją aktywacji ReLU.
network.add(layers.Dense(units=91, activation='relu', kernel_regularizer=regularizers.l2(0.01)))
# Dodanie warstwy wyjsciowej
network.add(layers.Dense(units=1, activation = 'sigmoid'))
# Kompilacja sieci neuronowej. 
network.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
# Wytrenowanie sieci neuronowej.
history = network.fit(X_train, # Cechy.
                      Y_train, # Wektor docelowy.
                      epochs=100,
                      verbose=1, # opis
                      validation_data=(X_test, Y_test))

# predykcja
Y_pred = network.predict(X_test)
# wizualizacja funkcji straty
training_loss = history.history["loss"] 
test_loss = history.history["val_loss"]

epoch_count = range(1, len(training_loss) + 1)

plt.plot(epoch_count, training_loss, "r--")
plt.plot(epoch_count, test_loss, "b-")
plt.legend(["Strata zbioru uczącego", "Strata zbioru testowego"]) 
plt.xlabel("Epoka")
plt.ylabel("Strata")
plt.show()

# z wykresu wynika, że optymalna bylaby liczba ok 10 epok. Model łatwo się przeucza.

# wizualizacja dokladnosci
training_accuracy = history.history["accuracy"] 
test_accuracy = history.history["val_accuracy"] 
plt.plot(epoch_count, training_accuracy, "r--") 
plt.plot(epoch_count, test_accuracy, "b-")

plt.legend(["Dokładność zbioru uczącego", "Dokładność zbioru testowego"]) 
plt.xlabel("Epoka")
plt.ylabel("Wynik dokładności")
plt.show();

# budowanie modelu
network = models.Sequential()
# Dodanie warstwy wejsciowej z funkcją aktywacji ReLU
network.add(layers.Dense(units=91, activation='relu', input_shape=(91,)))
# Dodanie warstwy ukrytej z funkcją aktywacji ReLU.
network.add(layers.Dense(units=91, activation='relu', kernel_regularizer=regularizers.l2(0.01)))
# Dodanie warstwy wyjsciowej
network.add(layers.Dense(units=1, activation = 'sigmoid'))
# Kompilacja sieci neuronowej. 
network.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
# Zakonczenie procesu uczenia w momencie zwiekszajacej sie straty zbioru testowego i zapis najlepszego modelu
callbacks = [EarlyStopping(monitor="val_loss", patience=2), ModelCheckpoint(filepath="best_model.h5",
monitor="val_loss", save_best_only=True)]
# Wytrenowanie sieci neuronowej.
history = network.fit(X_train, # Cechy.
                      Y_train, # Wektor docelowy.
                      epochs=10,
                      verbose=1, # opis
                      validation_data=(X_test, Y_test))

# predykcja
Y_pred = network.predict(X_test)

y_pred = network.predict(X_test) > 0.5
mat = confusion_matrix(Y_test, y_pred)
 
sns.heatmap(mat, square=True, annot=True, fmt='d', cbar=False, cmap='Blues')
 
plt.xlabel('Predicted label')
plt.ylabel('Actual label')

print(accuracy_score(Y_test, y_pred))

# logistic regression

log_reg = LogisticRegression()
log_reg.fit(X_train, Y_train)
Y_pred = log_reg.predict(X_test)

cm = confusion_matrix(Y_test, Y_pred)
plot_confusion_matrix(cm)

print(accuracy_score(Y_test, Y_pred))

classifier = SVC(kernel='sigmoid')
classifier.fit(X_train, Y_train)

# predykcja
Y_pred = classifier.predict(X_test)

# wyniki
cm = confusion_matrix(Y_test, Y_pred)
plot_confusion_matrix(cm)
print(accuracy_score(Y_test, Y_pred))

# wyniki okazały się niemal identyczne. Tylko SVR odstawał względem innych, testowanie innych hiperparametrów 
# mogłoby poprawić skuteczność.