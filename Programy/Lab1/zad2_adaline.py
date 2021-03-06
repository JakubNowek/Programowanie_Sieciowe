import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mlxtend.plotting import plot_decision_regions


class AdalineSGD(object):  # stochastic gradient descent

    def __init__(self, eta=0.01, epochs=50):
        self.eta = eta
        self.epochs = epochs

    def train(self, X, y, reinitialize_weights=True):

        if reinitialize_weights:
            self.w_ = np.zeros(1 + X.shape[1])
        self.cost_ = []

        for i in range(self.epochs):
            for xi, target in zip(X, y):
                output = self.net_input(xi)
                error = (target - output)
                self.w_[1:] += self.eta * xi.dot(error)
                self.w_[0] += self.eta * error

            cost = ((y - self.activation(X)) ** 2).sum() / 2.0
            self.cost_.append(cost)
        return self

    def net_input(self, X):
        return np.dot(X, self.w_[1:]) + self.w_[0]

    def activation(self, X):
        return self.net_input(X)

    def predict(self, X):
        return np.where(self.activation(X) >= 0.0, 1, -1)


# pobieranie danych w formacie csv
df = pd.read_csv('iris.data', header=None)

# wydzielenie danych treningowych
df_set = df.iloc[:40]
df_ver = df.iloc[50:90]
df_vir = df.iloc[100:140]
df_training = pd.concat([df_set, df_ver, df_vir], ignore_index=True)  # zbiór treningowy - 40x40x40

# wydzielenie danych testowych
test_df_set = df.iloc[40:50]
test_df_ver = df.iloc[90:100]
test_df_vir = df.iloc[140:150]
df_test = pd.concat((test_df_set, test_df_ver, test_df_vir), ignore_index=True)  # zbiór testowy 10x10x10


flower_class = 'Iris-virginica'
short_for_class = flower_class[5:8]
# setosa vs versicolor i virginica
y_training = df_training.iloc[0:120, 4].values  # 100 elementów z 4 kolumny (numeracja od 0) czyli kolumny z nazwą
y_training = np.where(y_training == flower_class, -1, 1)  # jeśli 'Iris-setosa' zwróć -1, jeśli nie daj 1

# Tworzenie zbioru treningowego i testowego - pobieranie długości kielicha i płatka (kolumny 0 i 2)
X_training = df_training.iloc[0:120, [0, 1, 2, 3]].values
X_test = df_test.iloc[0:30, [0, 1, 2, 3]].values

# Standaryzowanie danych
# standaryzowanie zbioru uczącego
X_train_std = np.copy(X_training)
X_train_std[:,0] = (X_training[:,0] - X_training[:,0].mean()) / X_training[:,0].std()
X_train_std[:,1] = (X_training[:,1] - X_training[:,1].mean()) / X_training[:,1].std()
X_train_std[:,2] = (X_training[:,2] - X_training[:,2].mean()) / X_training[:,2].std()
X_train_std[:,3] = (X_training[:,3] - X_training[:,3].mean()) / X_training[:,3].std()
# standaryzowanie zbioru treningowego
X_test_std = np.copy(X_test)
X_test_std[:, 0] = (X_test[:, 0] - X_test[:, 0].mean()) / X_test[:, 0].std()
X_test_std[:, 1] = (X_test[:, 1] - X_test[:, 1].mean()) / X_test[:, 1].std()
X_test_std[:, 2] = (X_test[:, 2] - X_test[:, 2].mean()) / X_test[:, 2].std()
X_test_std[:, 3] = (X_test[:, 3] - X_test[:, 3].mean()) / X_test[:, 3].std()
# część wykonawcza
ada = AdalineSGD(epochs=10, eta=0.0001)
# train and adaline and plot decision regions
ada.train(X_train_std, y_training)

plt.figure(figsize=(15, 6))
plt.subplots_adjust(wspace=0.3)
plt.subplot(1, 2, 1)

ada_output = ada.net_input(X_test_std)  # o(x)

# plt.subplot(1,2,1)
plt.plot(range(1, len(ada_output)+1), ada_output, marker='o')
plt.title('Adaline - o(x) dla z ze zboru walidacyjnego')
plt.xlabel('indeks x ze zbioru walidacyjnego')
plt.ylabel('o(x)')
#plt.show()

# testowanie


wynik = list(np.where(ada.predict(X_test_std) == -1, short_for_class, 'other'))


plt.subplot(1,2,2)
plt.plot(range(1, len(ada.cost_)+1), ada.cost_, marker='o')
plt.title('Wartość błędu w zależności od ilości iteracji')
plt.xlabel('Ilość iteracji')
plt.ylabel('Sum-squared-error')

tytul = "Model Adaline dla: epochs = {0}, eta = {1}". format(ada.epochs, ada.eta)
plt.suptitle(tytul)
plt.show()

print("Epochs = ", ada.epochs, "Eta = ", ada.eta)
print("Co przewidział klasyfikator")
print(list(ada.predict(X_test_std)))
print('Wynik:')
print(wynik[:10])
print(wynik[10:20])
print(wynik[20:30])

