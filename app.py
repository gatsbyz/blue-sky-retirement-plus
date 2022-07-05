# -*- coding: utf-8 -*-
"""Loan Qualifier Application.

This is a command line application to match applicants with qualifying loans.

Example:
    $ python app.py
"""
# The following Imports will import Library's that will be needed for the application.
# CSV imports and exports CSV files, sys will be used to exit the application if needed,
# Fire converts the application code into a Command Line Interface,
# Questionary allows for user input from the terminal into the application,
# Path allows us to use the paths of folders and documents within the application.

import csv
import sys
import fire
import questionary
from pathlib import Path

from qualifier.utils.fileio import load_csv, save_csv

from qualifier.utils.calculators import (
    calculate_monthly_debt_ratio,
    calculate_loan_to_value_ratio,
)


# The Filters will be used to remove pieces of data based on the parameters which will be input by the user.


from qualifier.filters.max_loan_size import filter_max_loan_size
from qualifier.filters.credit_score import filter_credit_score
from qualifier.filters.debt_to_income import filter_debt_to_income
from qualifier.filters.loan_to_value import filter_loan_to_value

# The following function will load the CSV file based on where the user points the questionary input to.

def load_bank_data():
    """Ask for the file path to the latest banking data and load the CSV file.

    Returns:
        The bank data from the data rate sheet CSV file.
    """

    csvpath = questionary.text("Enter a file path to a rate-sheet (.csv):").ask()
    csvpath = Path(csvpath)
    if not csvpath.exists():
        sys.exit(f"Ooops Cannot find this path:{csvpath}")

    return load_csv(csvpath)

# "This function get_applicant_info()" will use questionary to prompt questions that the user will input.
# The users input will prompt the next question.  Some questions require the user to press Enter while others will populate immediately after input.



def get_applicant_info():
    """Prompt dialog to get the applicant's financial information.

    Returns:
        Returns the applicant's financial information.
    """

    credit_score = questionary.text("What's your credit score?").ask()
    debt = questionary.text("What's your current amount of monthly debt?").ask()
    income = questionary.text("What's your total monthly income?").ask()
    loan_amount = questionary.text("What's your desired loan amount?").ask()
    home_value = questionary.text("What's your home value?").ask()

    credit_score = int(credit_score)
    debt = float(debt)
    income = float(income)
    loan_amount = float(loan_amount)
    home_value = float(home_value)

    return credit_score, debt, income, loan_amount, home_value

# The function will upload the Users input so that the loan csv (loan_rate_sheet.csv) will filter out any loans that wouldn't be granted to the user. 
  
def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):
    """Determine which loans the user qualifies for.

    Loan qualification criteria is based on:
        - Credit Score
        - Loan Size
        - Debit to Income ratio (calculated)
        - Loan to Value ratio (calculated)

    Args:
        bank_data (list): A list of bank data.
        credit_score (int): The applicant's current credit score.
        debt (float): The applicant's total monthly debt payments.
        income (float): The applicant's total monthly income.
        loan (float): The total loan amount applied for.
        home_value (float): The estimated home value.

    Returns:
        A list of the banks willing to underwrite the loan.

    """

    # Calculate the monthly debt ratio
    monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)
    print(f"The monthly debt to income ratio is {monthly_debt_ratio:.02f}")

    # Calculate loan to value ratio
    loan_to_value_ratio = calculate_loan_to_value_ratio(loan, home_value)
    print(f"The loan to value ratio is {loan_to_value_ratio:.02f}.")

    # Run qualification filters
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)

    print(f"Found {len(bank_data_filtered)} qualifying loans")

    return bank_data_filtered

# The Save_qualifying_loans funciton creates a input for the user to export a CSV for possible loans.
# If there are no qualifying loans the user will be notified and the application will be exited using sys.exit.


def save_qualifying_loans(qualifying_loans):
    """Saves the qualifying loans to a CSV file.

    Args:
        qualifying_loans (list of lists): The qualifying bank loans.
    """
    # @TODO: Complete the usability dialog for savings the CSV Files.
    if not qualifying_loans:
        sys.exit("Sorry, there are not qualifying loans.")

    save_File = questionary.confirm("Are you sure you want to save the qualifying loans?").ask()

    header = ['Lender','Max Loan Amount','Max LTV','Max DTI','Min Credit Score','Interest Rate']

    if save_File:
        csvpath = questionary.text("Please enter a filepath for the saved data:").ask()
        save_csv(Path(csvpath), qualifying_loans, header)


# The following function will be within the fire function and runs the script from start to finish.
# All parts of the application are brought together within the run() funciton to run with fire.

def run():
    """The main function for running the script."""

    # Load the latest Bank data
    bank_data = load_bank_data()

    # Get the applicant's information
    credit_score, debt, income, loan_amount, home_value = get_applicant_info()

    # Find qualifying loans
    qualifying_loans = find_qualifying_loans(
        bank_data, credit_score, debt, income, loan_amount, home_value
    )

    # Save qualifying loans
    save_qualifying_loans(qualifying_loans)

# Fire makes all the functions available in the command line using the function below.

if __name__ == "__main__":
    fire.Fire(run)
