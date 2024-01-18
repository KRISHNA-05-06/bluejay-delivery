%reload_ext autoreload
%autoreload 2

import pandas as pd

def analyze_employee_data(file_path, output_file='output.txt'):
    # Load the Excel file into a pandas DataFrame
    df = pd.read_excel(file_path)

    # Updated column names based on the provided headings
    position_id_column = 'Position ID'
    position_sta_column = 'Position Sta'
    time_column = 'Time'
    time_out_column = 'Time Out'
    timecard_hours_column = 'Timecard Ho'
    pay_cycle_start_column = 'Pay Cycle St'
    pay_cycle_end_column = 'Pay Cycle E'
    employee_name_column = 'Employee Name'
    file_number_column = 'File Number'

    # Convert 'Time' and 'Time Out' columns to datetime type with format
    df[time_column] = pd.to_datetime(df[time_column], format='%m/%d/%Y %H', errors='coerce')
    df[time_out_column] = pd.to_datetime(df[time_out_column], format='%m/%d/%Y %H', errors='coerce')

    # (a) Find employees who worked for 7 consecutive days
    consecutive_days = 7
    result_df_a = df.groupby(position_id_column)[time_column].apply(lambda x: x.diff().dt.days == 1).groupby(df[position_id_column]).sum()
    result_df_a = result_df_a[result_df_a >= consecutive_days].reset_index()

    # (b) Employees with less than 10 hours between shifts but greater than 1 hour
    less_than_10_hours = (
        (df.groupby(position_id_column)[time_column].diff().dt.total_seconds() / 3600 < 10) &
        (df.groupby(position_id_column)[time_column].diff().dt.total_seconds() / 3600 > 1)
    )
    result_df_b = df[less_than_10_hours].groupby(position_id_column).first().reset_index()

    # (c) Employees who worked for more than 14 hours in a single shift
    more_than_14_hours = (
        df.groupby(position_id_column)[time_out_column].transform(lambda x: x.sub(x.shift(1))).dt.total_seconds() / 3600 > 14
    )
    result_df_c = df[more_than_14_hours].groupby(position_id_column).first().reset_index()

    # Write the results to the output file
    with open(output_file, 'w') as output:
        # Results for (a)
        output.write("Employees who worked for 7 consecutive days:\n")
        if not result_df_a.empty:
            for index, row in result_df_a.iterrows():
                employee_info = df.loc[df[position_id_column] == row[position_id_column], [employee_name_column, position_sta_column]].iloc[0]
                output.write(f"Name: {employee_info[employee_name_column]}, Position: {row[position_sta_column]}\n")
        else:
            output.write("NA\n")

        # Results for (b)
        output.write("\nEmployees with less than 10 hours between shifts but greater than 1 hour:\n")
        if not result_df_b.empty:
            for index, row in result_df_b.iterrows():
                employee_info = df.loc[df[position_id_column] == row[position_id_column], [employee_name_column, position_sta_column]].iloc[0]
                output.write(f"Name: {employee_info[employee_name_column]}, Position: {row[position_sta_column]}\n")
        else:
            output.write("NA\n")

        # Results for (c)
        output.write("\nEmployees who worked for more than 14 hours in a single shift:\n")
        if not result_df_c.empty:
            for index, row in result_df_c.iterrows():
                employee_info = df.loc[df[position_id_column] == row[position_id_column], [employee_name_column, position_sta_column]].iloc[0]
                output.write(f"Name: {employee_info[employee_name_column]}, Position: {row[position_sta_column]}\n")
        else:
            output.write("NA\n")

# Replace 'your_file.xlsx' with the actual path to your Excel file
file_path = "C:/Users/KOTA SRIKRISHNA SAI/OneDrive/Desktop/bluejay assignment/input.xlsx"
analyze_employee_data(file_path, output_file='output.txt')
