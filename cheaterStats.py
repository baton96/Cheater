import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
out = pd.read_csv('cheaterStats.csv')
out.plot(x ='Liczba wygranych z kolejnymi graczami (na 100 rozegranych gier)', y='Średnia liczba sprawdzeń każdego z graczy', kind = 'scatter')
plt.show()
out.plot(x ='Liczba wygranych z kolejnymi graczami (na 100 rozegranych gier)', y='Średnia liczba Twoich oszustw na grę z każdym z graczy', kind = 'scatter')
plt.show()
out.plot(x ='Średnia liczba Twoich oszustw na grę z każdym z graczy', y='Średnia liczba sprawdzeń każdego z graczy', kind = 'scatter')
plt.show()
#threedee = plt.figure().gca(projection='3d')
#threedee.scatter(df['Średnia liczba sprawdzeń każdego z graczy'], df['Średnia liczba Twoich oszustw na grę z każdym z graczy'], df['Liczba wygranych z kolejnymi graczami (na 100 rozegranych gier)'])
