import pickle
import numpy as np

pickle_model = '/Users/Stephen/Desktop/Computer Science/Semester 2/Software Engineering/Assignment/Project/Workspace/DublinBikes/analytics/PARNELL_SQUARE_NORTH.sav'

loaded_model = pickle.load(open(pickle_model, 'rb'))
result = loaded_model.predict([['1030', 1]])
result = int(result)
print(result)
