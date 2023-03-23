import numpy
import pandas
from sklearn.model_selection import train_test_split


### Szukane wartości a i b regresji y = ax + b zapiszemy w tablicy theta


### Funkcja regresji a = theta[1], b = theta[0] - nasza hipoteza h
def linearRegression(theta, x):
    return theta[0] + theta[1] * x


### Funkcja kosztu - nasza funkcja J
def costFunction(h, theta, x, y):
    m = len(y)
    return 1.0 / (2 * m) * sum((h(theta, x[i]) - y[i])**2 for i in range(m))


### Funkcja wyznaczająca optymalne wartości a i b funkcji regresji y = ax + b
def gradient_descent(h, cost_function, theta, x, y, alpha, eps):
    current_cost = cost_function(h, theta, x, y)
    m = len(y)
    while True:
        new_theta = [
            theta[0] - alpha / float(m) * sum(h(theta, x[i]) - y[i] for i in range(m)),
            theta[1] - alpha / float(m) * sum((h(theta, x[i]) - y[i]) * x[i] for i in range(m))
        ]
        theta = new_theta
        try:
            current_cost, prev_cost = cost_function(h, theta, x, y), current_cost
        except OverflowError:
            break
        if abs(prev_cost - current_cost) <= eps:
            break
        print("\n------------------------------------------\n")
        print("Obecny koszt: " + str(current_cost))
        print("Poprzedni koszt: " + str(prev_cost))
        print("Zmiana kosztu: " + str(prev_cost - current_cost))
        print("Aktualna funkcja regresji: y = " + str(theta[1]) + "x + " + str(theta[0]))
    return theta


### Funkcja standaryzująca
def standardize(val):
    return (val - numpy.mean(val)) / numpy.std(val)


def main():
    numpy.seterr(over='raise')

    ### Wczytanie zbioru danych
    houses = pandas.read_csv('mieszkania.tsv', sep='\t')

    ### Podział na zbiór uczący i testowy
    y = houses['cena']
    x = houses['Powierzchnia w m2']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    ### Standaryzujemy zbiór uczący
    X = standardize(x_train)
    X = X.reset_index(drop=True)
    print(X)

    ### Wybieramy ze zbioru uczącego wartości zmiennej, którą przewidujemy
    y = y_train.values
    print(y)

    ### Uruchamiamy algorytm gradientu prostego do wyznaczenia optymalnych wartości a i b dla funkcji regresji y = ax + b
    best_theta = gradient_descent(linearRegression, costFunction, [0.0, 0.0], X, y, alpha=0.01, eps=0.01)

    ### Gdy już mamy funkcję regresji, możemy przewidywać ceny mieszkań dla innych wartości naszej informacji
    x_test = standardize(x_test)
    x_test = x_test.reset_index(drop=True)
    predictions = linearRegression(best_theta, x_test)
    print(predictions)


main()
