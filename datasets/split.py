import pandas as pd
from sklearn.model_selection import train_test_split
import sys

data = pd.read_csv(sys.argv[1])

train, test = train_test_split(data, shuffle=True)

train.to_csv('train.csv',index=False)
test.to_csv('test.csv',index=False)
