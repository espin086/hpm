import streamlit as st

from gpt import generate_completion

import config


HOW_TO_SUMMARIZE = """ You need to provide an python code. 


Requirements for Code:

- Produce Docstrings for the module, classes, and functions, using the Google Docstring Format.
- Ensure usage of classes and best practices of object-oriented programming. YOu want to have a class that is responsible for the main functionality of the code.
- Develop a main function that uses the classes that accepts useful and important command line arguments viaargparse(not sys).
- Operate logging for methods, functions, etc., using the logging library and consistent logging of info, warning, error, etc. where practical.
- Format the generated code beautifully following the Black standard.
- Can you provide a diagram showing how the code works? Say a sequence diagram, flowchart, or a UML diagram as well, this is required

Note: I have a set of classes already that I can import to make the code more modular and easier to write. Here are the classes I have:

Name: sqlitecrud.py

Code: import sqlite3


class SQLiteCRUD:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            return True
        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")
            return False

    def create_table(self, table_name, columns):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                column_str = ", ".join(columns)
                create_table_query = (
                    f"CREATE TABLE IF NOT EXISTS {table_name} ({column_str})"
                )
                cursor.execute(create_table_query)
                self.connection.commit()
                return True
            else:
                print("Database connection is not established.")
                return False
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
            return False

    def insert_data(self, table_name, data):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                placeholders = ", ".join(["?"] * len(data))  # removed +1 for the uuid
                insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
                cursor.execute(insert_query, data)  # removed uuid from data
                self.connection.commit()
                return True
            else:
                print("Database connection is not established.")
                return False
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")
            return False

    def select_data(self, table_name, condition=None):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                if condition:
                    select_query = f"SELECT * FROM {table_name} WHERE {condition}"
                else:
                    select_query = f"SELECT * FROM {table_name}"
                cursor.execute(select_query)
                return cursor.fetchall()
            else:
                print("Database connection is not established.")
                return []
        except sqlite3.Error as e:
            print(f"Error selecting data: {e}")
            return []

    def update_data(self, table_name, data, condition):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                set_values = ", ".join([f"{key} = ?" for key in data.keys()])
                update_query = f"UPDATE {table_name} SET {set_values} WHERE {condition}"
                cursor.execute(update_query, list(data.values()))
                self.connection.commit()
                return True
            else:
                print("Database connection is not established.")
                return False
        except sqlite3.Error as e:
            print(f"Error updating data: {e}")
            return False

    def delete_data(self, table_name, condition):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                delete_query = f"DELETE FROM {table_name} WHERE {condition}"
                cursor.execute(delete_query)
                self.connection.commit()
                return True
            else:
                print("Database connection is not established.")
                return False
        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")
            return False

    def close(self):
        if self.connection:
            self.connection.close()


Name: csvhandler.py

Code: 

import pandas as pd
import os


class CSVHandler:
    def __init__(self, file_path, delimiter=","):
        self.file_path = file_path
        self.delimiter = delimiter
        self.dataframe = None

        # Check if file exists, if not create it
        if not os.path.isfile(self.file_path):
            open(self.file_path, "w").close()

    def read_csv(self):
        ""
        Read the CSV file with the specified delimiter.

        :return: DataFrame containing the CSV data.
        ""
        try:
            self.dataframe = pd.read_csv(self.file_path, delimiter=self.delimiter)
            return self.dataframe
        except Exception as e:
            print(f"Error reading CSV file: {e}")

    def save_csv(self, df, index=False):
        ""
        Save a DataFrame to the CSV file with the specified delimiter.

        :param df: DataFrame to save.
        :param index: Boolean flag to include index in CSV. Default is False.
        ""
        try:
            df.to_csv(self.file_path, delimiter=self.delimiter, index=index)
            self.dataframe = df
        except Exception as e:
            print(f"Error saving CSV file: {e}")

    def append_csv(self, df, index=False):
        ""
        Append a DataFrame to the existing CSV file with the specified delimiter.

        :param df: DataFrame to append.
        :param index: Boolean flag to include index in CSV. Default is False.
        ""
        try:
            df.to_csv(
                self.file_path,
                mode="a",
                header=False,
                delimiter=self.delimiter,
                index=index,
            )
            if self.dataframe is not None:
                self.dataframe = pd.concat([self.dataframe, df], ignore_index=True)
            else:
                self.dataframe = df
        except Exception as e:
            print(f"Error appending to CSV file: {e}")

    def update_csv(self, df, index=False):
        ""
        Update the CSV file with a new DataFrame, overwriting existing content.

        :param df: DataFrame to save.
        :param index: Boolean flag to include index in CSV. Default is False.
        ""
        self.save_csv(df, index=index)
        self.dataframe = df

    def get_dataframe(self):
        ""
        Get the DataFrame of the CSV data.

        :return: DataFrame containing the CSV data.
        ""
        return self.dataframe

        
Name: streamlithandler.py

Code: 

import streamlit as st
import pandas as pd
import plotly.express as px
import logging
from argparse import ArgumentParser
from sqlitecrud import SQLiteCRUD
from csvhandler import CSVHandler


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class StreamlitApp:
    ""
    A template class for creating Streamlit applications with a sidebar and interactive data exploration.

    Attributes:
        title (str): The title of the Streamlit application.
        csv_handler (CSVHandler): An instance of the CSVHandler for CSV operations.
        db_handler (SQLiteCRUD): An instance of the SQLiteCRUD for database operations.
    ""

    def __init__(self, title: str, csv_file: str, db_name: str):
        ""
        Initializes the StreamlitApp with a title, CSV file, and SQLite database.

        Args:
            title (str): The title of the Streamlit application.
            csv_file (str): The path to the CSV file for data operations.
            db_name (str): The name of the SQLite database for data operations.
        ""
        self.title = title
        self.csv_handler = CSVHandler(csv_file)
        self.db_handler = SQLiteCRUD(db_name)
        st.set_page_config(page_title=title)
        self.setup_sidebar()

    def setup_sidebar(self):
        ""Sets up the sidebar for the Streamlit application.""
        st.sidebar.title("Navigation")
        selections = st.sidebar.radio("Go to", ["Home", "Data Sample", "Plots"])
        if selections == "Home":
            self.home_page()
        elif selections == "Data Sample":
            self.data_sample_page()
        elif selections == "Plots":
            self.plots_page()

    def home_page(self):
        ""Displays the Home page.""
        st.title(self.title)
        st.write("Welcome to the Streamlit application template!")
        logging.info("Home page displayed.")

    def data_sample_page(self):
        ""Displays the Data Sample page with the contents of the CSV.""
        st.title("Data Sample")
        dataframe = self.csv_handler.read_csv()
        st.write("Below is a sample of the CSV data:")
        st.dataframe(dataframe)
        st.write("Dataframe Info:")
        st.write(dataframe.info())
        st.write("Dataframe Description:")
        st.write(dataframe.describe())
        logging.info("Data Sample page displayed with data from CSV.")

    def plots_page(self):
        ""Displays the Plots page for interactive plotly graphs.""
        st.title("Interactive Plots")
        dataframe = self.csv_handler.read_csv()
        if dataframe is not None and not dataframe.empty:
            columns = dataframe.columns.tolist()
            x_axis = st.selectbox("X-axis", columns)
            y_axis = st.selectbox("Y-axis", columns)
            plot = px.scatter(dataframe, x=x_axis, y=y_axis)
            st.plotly_chart(plot)
            logging.info("Plots page displayed with interactive plots.")
        else:
            st.write("No data available to plot.")
            logging.warning("No data available to plot in the Plots page.")

    def run(self):
        ""Runs the Streamlit application.""
        logging.info("Streamlit application is running.")
        st.title(self.title)
        st.write("Use the sidebar to navigate through the app.")


def main():
    parser = ArgumentParser(description="Streamlit Multipage Application Template")
    parser.add_argument("--title", type=str, default="Streamlit App", help="The title of the app.")
    parser.add_argument("--csv_file", type=str, required=True, help="Path to the CSV file.")
    parser.add_argument("--db_name", type=str, required=True, help="SQLite database name.")
    args = parser.parse_args()

    app = StreamlitApp(title=args.title, csv_file=args.csv_file, db_name=args.db_name)
    app.run()


if __name__ == "__main__":
    main()

    
Name: gpt.py

Code: 

""

This is a GPT text generation module. It is used to generate text based on a prompt.

""


import openai
import streamlit as st

openai.api_key = st.secrets["openai"]["key"]
openai.organization = st.secrets["openai"]["org"]


def generate_completion(model, role, prompt):
    ""
    This function generates text based on a prompt.
    ""
    completion = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": prompt},
        ],
    )
    return completion.choices[0].message["content"]

Name: excel.py


Code: 

import pandas as pd
import logging
import argparse


class ExcelHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.dataframes = {}
        self.logger = logging.getLogger(__name__)

    def read_sheet(self, sheet_name):
        ""
        Read a specific sheet from the Excel file.

        :param sheet_name: Name of the sheet to read.
        :return: DataFrame containing the sheet data.
        ""
        try:
            df = pd.read_excel(self.file_path, sheet_name=sheet_name)
            self.dataframes[sheet_name] = df
            self.logger.info(f"Read sheet '{sheet_name}' successfully.")
            return df
        except Exception as e:
            self.logger.error(f"Error reading sheet {sheet_name}: {e}")

    def read_all_sheets(self):
        ""
        Read all sheets from the Excel file.

        :return: Dictionary with sheet names as keys and DataFrames as values.
        ""
        try:
            xls = pd.ExcelFile(self.file_path)
            for sheet_name in xls.sheet_names:
                self.dataframes[sheet_name] = pd.read_excel(xls, sheet_name=sheet_name)
            self.logger.info("Read all sheets successfully.")
            return self.dataframes
        except Exception as e:
            self.logger.error(f"Error reading all sheets: {e}")

    def save_sheet(self, df, sheet_name):
        ""
        Save a DataFrame to a specific sheet in the Excel file.

        :param df: DataFrame to save.
        :param sheet_name: Name of the sheet to save the DataFrame to.
        ""
        try:
            with pd.ExcelWriter(
                self.file_path, engine="openpyxl", mode="a", if_sheet_exists="replace"
            ) as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            self.dataframes[sheet_name] = df
            self.logger.info(f"Saved sheet '{sheet_name}' successfully.")
        except Exception as e:
            self.logger.error(f"Error saving sheet {sheet_name}: {e}")

    def save_all_sheets(self):
        ""
        Save all DataFrames in the dataframes dictionary to the Excel file.
        ""
        try:
            with pd.ExcelWriter(self.file_path, engine="openpyxl") as writer:
                for sheet_name, df in self.dataframes.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            self.logger.info("Saved all sheets successfully.")
        except Exception as e:
            self.logger.error(f"Error saving all sheets: {e}")

    def get_dataframe(self, sheet_name):
        ""
        Get the DataFrame of a specific sheet.

        :param sheet_name: Name of the sheet.
        :return: DataFrame containing the sheet data.
        ""
        return self.dataframes.get(sheet_name, None)

    def list_sheets(self):
        ""
        List all sheet names in the Excel file.

        :return: List of sheet names.
        ""
        try:
            xls = pd.ExcelFile(self.file_path)
            self.logger.info("Listed all sheets successfully.")
            return xls.sheet_names
        except Exception as e:
            self.logger.error(f"Error listing sheets: {e}")
            return []


def main(file_path):
    # Initialize logging
    logging.basicConfig(level=logging.INFO)

    # Instantiate ExcelHandler
    excel_handler = ExcelHandler(file_path)

    # Read all sheets
    sheets = excel_handler.read_all_sheets()
    print("Sheets:", sheets)

    # List all sheets
    sheet_names = excel_handler.list_sheets()
    print("Sheet Names:", sheet_names)

    # Save all sheets
    for sheet_name, df in sheets.items():
        excel_handler.save_sheet(df, sheet_name)
    excel_handler.save_all_sheets()


if __name__ == "__main__":
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(description="Excel Handler")
    parser.add_argument("file_path", type=str, help="Path to the Excel file")

    # Parse command-line arguments
    args = parser.parse_args()

    # Call main function with the provided file path
    main(args.file_path)




You can use these classes to make the code more modular and easier to write. You just write the main function that uses these classes to complete the task.

Note you don't need to explain any of the code, but I do need you to write the code that will complete the task. As well as the classes that where imported that I shared with you above, if they are used in the main.py that you will write.

Also include the directory structure of the code you write.


"""


def render_text_area(section_title, help_text):
    """Render a text area component in the Streamlit app.

    Parameters:
        section_title (str): The title for this section.
        help_text (str): The help text for the text area.

    Returns:
        str: The text entered by the user in the text area.
    """
    return st.text_area("", help=help_text, key=section_title)


def render_summary_button():
    """Render a button for summarizing the input.

    Returns:
        bool: True if the button is clicked, False otherwise.
    """
    return st.button("Write Code", key="btn_summarize")


def get_summary(model, role, prompt):
    """Get a summary text generated by GPT.

    Parameters:
        model (str): The GPT model to use.
        role (str): The role description for the prompt.
        prompt (str): The prompt text to summarize.

    Returns:
        str: The generated summary text.
    """
    return generate_completion(model, role, prompt)


def main():
    """Main function to render the Streamlit app."""

    st.header("What should code do?")
    feature_input = render_text_area(
        "What should the code do?",
        "What is the specific issue or feature that the code needs to implement?",
    )
    st.write("---")

    st.header("Acceptance Criteria")
    acceptance_input = render_text_area(
        "Acceptance Criteria?",
        "What must the code do to be considered complete?",
    )
    st.write("---")

    prompt = f"""Here is your task {HOW_TO_SUMMARIZE}. 
    Here are the goals: {feature_input}. 
    
    acceptance criteria: {acceptance_input}.
    """

    if render_summary_button():
        summary = get_summary(config.GPT_MODEL, config.UserConfig().job_title, prompt)
        st.write(summary)


if __name__ == "__main__":
    main()
