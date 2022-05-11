import pandas as pd
# List of Tuples
students = [('jack', 34, 'Sydney', 155),
            ('Riti', 31, 'Delhi', 177.5),
            ('Aadi', 16, 'Mumbai', 81),
            ('Mohit', 31, 'Delhi', 167),
            ('Veena', 12, 'Delhi', 144),
            ('Shaunak', 35, 'Mumbai', 135),
            ('Shaun', 35, 'Colombo', 111)
            ]
# Create a DataFrame object
studentDfObj = pd.DataFrame(students, columns=['Name', 'Age', 'City', 'Score'])

listOfDFRows = studentDfObj.to_numpy().tolist()
print(listOfDFRows)
print(type(listOfDFRows))