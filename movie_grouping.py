import pandas as pd
import numpy
from collections import OrderedDict

def union(A,B):
    result_set = dict()
    for A_key, B_key in zip(A,B):
        A_value = A[A_key]
        B_value = B[B_key]

        if A_value > B_value:
            result_set[A_key] = A_value
        else:
            result_set[B_key] = B_value
            
    sorted_set= {key: result_set[key] for key in sorted(result_set, key = lambda ele: result_set[ele], reverse = True)}
    
    return sorted_set


def intersection(A,B):
    result_set = dict()
    for A_key, B_key in zip(A,B):
        A_value = A[A_key]
        B_value = B[B_key]

        if A_value < B_value:
            result_set[A_key] = A_value
        else:
            result_set[B_key] = B_value
         
    sorted_set= {key: result_set[key] for key in sorted(result_set, key = lambda ele: result_set[ele], reverse = True)}

    return sorted_set
    

## calculating year of production
def new_films(x):
    if x <= 2016:
        return 0
    elif x > 2016:
        return (float(x)/2022)

def old_films(x):
    if x >= 1999:
        return 0
    elif x < 1999:
        return 1 - (float(x)/1990)

def avg_old_films(x):
    if x <= 1999 or x >= 2018:
        return 0
    elif 1999 < x and x < 2018:
        return 1-(float(abs(2008-x))/2008)

### calculating film length 
def long_films(x):
    if x <= 100:
        return 0
    elif x > 100:
        return (float(x)/180)

def short_films(x):
    if x >= 120:
        return 0
    if x < 120:
        return 1 - (float(x)/100)

def avg_length_films(x):
    if x <= 60 or x >= 120:
        return 0
    elif 60 < x < 120:
        return 1-(float(abs(90-x))/90)

    
def main(): 
    df = pd.read_csv('Desktop/database.csv', delimiter=';')
    A = dict()
    B = dict()
    character = 'A'
    production_year = df['Rok produkcji']
    time = df['Czas']
    df.set_index('ID', inplace = True) 
    
    ## filmy stare i dość długie
    for index in range(len(production_year)):
        A[index + 1] = old_films(production_year[index])

    for index in range(len(time)):
        B[index + 1] = avg_length_films(time[index])
    
    intersection_result = intersection(A,B)
    
    films1 = pd.DataFrame()
    for i in intersection_result:
        films1[i] = df.loc[i]
    
    films1.to_csv('filmy_stare_i_dosc_dlugie.csv',encoding='utf8')  
    
    ## filmy średnio stare lub niedługie
    for index in range(len(production_year)):
        A[index + 1] = avg_old_films(production_year[index])

    for index in range(len(time)):
        B[index + 1] = short_films(time[index])
    
    union_result = union(A,B)
    
    films2 = pd.DataFrame()
    for i in union_result:
        films2[i] = df.loc[i]
    
    films2.to_csv('filmy_srednio_stare_lub_niedlugie.csv',encoding='utf8')      
    
    
    ## filmy w miarę nowe i średnio długie
    for index in range(len(production_year)):
        A[index + 1] = new_films(production_year[index])

    for index in range(len(time)):
        B[index + 1] = avg_length_films(time[index])
    
    intersection_result = intersection(A,B)
    
    films3 = pd.DataFrame()
    for i in intersection_result:
        films3[i] = df.loc[i]
    
    films3.to_csv('filmy_w_miare_nowe_i_srednio_dlugie.csv',encoding='utf8')   
    
    
main()

