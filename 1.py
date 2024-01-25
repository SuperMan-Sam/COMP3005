class EnhancedRelaxSystem:
    def __init__(self):
        self.tables = {}

    def add_table(self, table_name, columns, data):
        self.tables[table_name] = {'columns': columns, 'data': data}

    def select(self, table_name, condition):
        table = self.tables[table_name]
        selected_data = [row for row in table['data'] if condition(row)]
        return {'columns': table['columns'], 'data': selected_data}

    """ def project(self, table_name, selected_columns):
        table = self.tables[table_name]
        column_indices = [table['columns'].index(col) for col in selected_columns]
        projected_data = [[row[i] for i in column_indices] for row in table['data']]
        return {'columns': selected_columns, 'data': projected_data} """
    def project(self, table_name, selected_columns):
        table = self.tables[table_name]
        print(table_name)
        print(selected_columns)
        if len(selected_columns) == 1:
            column_index = table['columns'].index(selected_columns[0])
            projected_data = [[row[column_index]] for row in table['data']]
            return {'columns': selected_columns, 'data': projected_data}
        else:
            column_indices = [table['columns'].index(col) for col in selected_columns]
            projected_data = [[row[i] for i in column_indices] for row in table['data']]
            return {'columns': selected_columns, 'data': projected_data}


    def join(self, left_table, right_table, on_condition):
        if left_table not in self.tables:
            print(f"Table '{left_table}' does not exist.")
            return None
    
        if right_table not in self.tables:
            print(f"Table '{right_table}' does not exist.")
            return None
        left = self.tables[left_table]
        right = self.tables[right_table]
        joined_data = []
        for l_row in left['data']:
            for r_row in right['data']:
                joined_data.append(l_row + r_row)
        joined_columns = left['columns'] + right['columns']
        return {'columns': joined_columns, 'data': joined_data}


    def union(self, table1, table2):
        t1 = self.tables[table1]
        t2 = self.tables[table2]
        union_data = t1['data'] + [row for row in t2['data'] if row not in t1['data']]
        return {'columns': t1['columns'], 'data': union_data}

    def intersect(self, table1, table2):
        t1 = self.tables[table1]
        t2 = self.tables[table2]
        intersect_data = [row for row in t1['data'] if row in t2['data']]
        return {'columns': t1['columns'], 'data': intersect_data}

    def difference(self, table1, table2):
        t1 = self.tables[table1]
        t2 = self.tables[table2]
        difference_data = [row for row in t1['data'] if row not in t2['data']]
        return {'columns': t1['columns'], 'data': difference_data}

system = EnhancedRelaxSystem()

employees_data = [
    ["E1", "John", 32],
    ["E2", "Alice", 28],
    ["E3", "Bob", 29]
]
system.add_table("Employees", ["EID", "Name", "Age"], employees_data)

selected_employees = system.select("Employees", lambda row: row[2] > 30)
projected_employees = system.project("Employees", ["Name", "Age"])

another_table_data = [
    ["E1", "John", 32],
    ["E4", "Dave", 35]
]
system.add_table("AnotherTable", ["EID", "Name", "Age"], another_table_data)
print("------------------")
print(another_table_data)
print("------------------")
joined_data = system.join("Employees", "AnotherTable", lambda l_row, r_row: l_row[0] == r_row[0])

union_data = system.union("Employees", "AnotherTable")
intersect_data = system.intersect("AnotherTable", "Employees")
difference_data = system.difference("Employees", "AnotherTable")

print("Example for: \nEmployees (EID, Name, Age) = {\n    E1, John, 32\n    E2, Alice, 28\n    E3, Bob, 29\n}")
print("Example2 for: \nAnotherTable (EID, Name, Age) = {\n    E1, John, 32\n    E4, Dave, 35\n}")
print("select Age>30(Employees):")
print(selected_employees)
print("projected (Employees) by Name and Age:")
print(projected_employees)
print("joined (Employees) first row together:")
print(joined_data)
print("union (Employees) and (AnotherTable):")
print(union_data)
print("Find items from Employees that are different from AnotherTable:")
print(difference_data)
print("Find items from Employees that are same from AnotherTable:")
print(intersect_data)

table_name = input("Please enter table name:")
header = input("Please enter headers separated by commas (e.g:Name,Age): ")
header = header.split(",")
table_data = []

while True:
    row = input("Please enter rows of data, separated by commas (or enter 'exit' to exit): ")
    if row.lower() == 'exit':
        break
    
    row = row.split(",")
    
    if len(row) != len(header):
        print("The number of data row fields does not match the header length, please re-enter。")
        continue
    
    table_data.append(row)

print(table_data)
system.add_table(table_name, header, table_data)
print(table_data)
print("Your data is:")
print("Table name:", table_name)
for row in table_data:
    print(row)



query = input("Please enter one query you want(e.g: select or projection or join or union or difference or intersect):")
if query == 'select':
    filter_column = input("Please enter the filter column (e.g: Age): ")
    filter_operator = input("Please enter the filter operator (e.g: >, <, ==): ")
    filter_value = input("Please enter the filter value: ")
    def filter_function(row):
        try:
            # Get the index of the filter column
            column_index = system.tables[table_name]['columns'].index(filter_column)

            # Get the value from the row based on the column index
            value = row[column_index]

            # Check if the value is numeric and compare using the specified operator
            if value.isnumeric():
                return eval(f"{value} {filter_operator} {filter_value}")
            elif type(value) == str and filter_operator == '==':
                return value == filter_value
            else:
                print(f"Error: Invalid value ({value}) in the specified column.")
                return False
        except Exception as e:
            print("Error: ", e)
            return False

    selected_data = system.select(table_name, filter_function)
    print(selected_data)

elif query == 'projection':
    selected_columns = input("Please enter the columns to project (comma-separated, e.g: Age,Name): ").split(',')
    print(selected_columns)
    projected_data = system.project(table_name, selected_columns)
    print(projected_data)
elif query == 'join':
    left_table = input("Please enter the name of the first table: ")
    right_table = input("Please enter the name of the second table: ")

    joined_data = system.join(left_table, right_table, lambda l_row, r_row: l_row[0] == r_row[0])
    
    if joined_data is not None:
        print("Joined data:")
        print(joined_data)
elif query == 'union':
    left_table = input("Please enter the name of the first table: ")
    right_table = input("Please enter the name of the second table: ")

    unioned_data = system.union(left_table, right_table)
    
    if unioned_data is not None:
        print("Unioned data:")
        print(unioned_data)
elif query == 'difference':
    left_table = input("Please enter the name of the first table: ")
    right_table = input("Please enter the name of the second table: ")

    difference_data = system.difference(left_table, right_table)
    
    if difference_data is not None:
        print("Difference data:")
        print(difference_data)
elif query == 'intersect':
    left_table = input("Please enter the name of the first table: ")
    right_table = input("Please enter the name of the second table: ")

    intersect_data = system.intersect(left_table, right_table)
    
    if intersect_data is not None:
        print("Intersected data:")
        print(intersect_data)
    