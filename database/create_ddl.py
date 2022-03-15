#Author: Viswanadha-Aditya

import argparse
import os

import pandas as pd

accepted_columns = [
    "column_name" , "column name", "name",
    "datatype", "data_type", "column type", "column_type", "type",
    "comments", "column_comments", "column comments", "comment",
    "column comment", "column_comment"
]

def read_file(file_name, file_type='csv'):
    if file_type=='csv':
        df = pd.read_csv(file_name)
    elif file_type=="xls" or file_type=="xlsx":
        df = pd.read_excel(file_name)
    else:
        print(f"File type .{file_type} not supported")
    for column in df.columns:
        if column.lower() not in accepted_columns:
            df.drop(column, axis=1)
            continue
        if "name" in column.lower():
            df.rename({column:"column_name"})
        elif "type" in column.lower():
            df.rename({column:"data_type"})
        elif "comment" in column.lower():
            df.rename({column:"comment"})
        else:
            df.drop(column, axis=1)
            continue
    return df 

def create_ddl(df, table, replace, output_file):
    if os.path.isfile(output_file):
        op_file = open(output_file, "a")
    else:
        op_file = open(output_file, "w")
    if replace == 'N':
        print(f"CREATE TABLE {table} (", file=op_file)
    else:
        print(f"CREATE OR REPLACE TABLE {table} (", file=op_file)
    counter = 0
    for col in df.to_dict(orient='records'):
        if counter < len(df)-1:
            print(
                "\t"+
                f"{col['name']} {col['type']} COMMENT '{col['comment']}',",
                file=op_file
            )
        else:
            print(
                "\t"+
                f"{col['name']} {col['type']} COMMENT '{col['comment']}'", 
                file=op_file
            )
        counter += 1
    print(");\n", file=op_file)
    op_file.close()
    print(f"DDL created in {output_file}")
    return True


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", required=True)
    parser.add_argument("-t", "--table", required=True)
    parser.add_argument("-x", "--extension", required=False, default="csv")
    parser.add_argument(
        "-o", "--output", 
        required=False, 
        default="~/ddl_output.sql"
    )
    parser.add_argument(
        "-r", "--replace", 
        required=False, 
        default="N", choices=['Y', 'N']
    )
    args = parser.parse_args()

    file_name = args.file
    table = args.table 
    file_type = args.extension
    output_file = args.output
    replace = args.replace

    df = read_file(file_name, file_type)
    create_ddl(df, table, replace, output_file)

    print("Process Completed")
