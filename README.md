# Retirement Global 2.0

## How To Run
1. Open `RoboAdviser-LexJson.zip file` to start Amazon Lex chatbot
2. Enter the utterance: "I want to retire"
3. Follow and answer prompts from Amazon Lex chatbot
4. The CUI will show you the cities you can retire in.
5. Your retirement cities will be saved in `cache/retirement-cities.csv`
6. run `jupyter/retirement_tool.ipynb` to visualize your retirement data. the most recent user input will be used.
7. run `jupyter/map_retirement_cities.ipynb` to visualize your retirement cities. the most recent retirement cities will be used.
8. map results saved in `Interactive_retirement_map.html`
9. Retire!

## Sample Prompts (Amazon Lex)
? What is your current age 25

? By what age, would you prefer to retire? 65

? How much do you have in liquid cash savings (USD) 50000

? Would you like your portfolio to be conservative[1], conservatively moderate[2], or moderate[3]? 3

? How much would you like to invest in stocks and bonds? 40000

## Sample Output/Response
You can retire in
['Paris/France', 'Hamilton/Canada', 'Milan/Italy', 'Bucaramanga/Colombia', 'Madrid/Spain', 'Delhi/India']


# Executive Summary

Retirement Global 2.0 is our new and improved application designed to help working class citizens live out their dream retirement sooner. In addition to our original promise, we seek to provide our clients with new products to help them build wealth. The new Housing Analytics tool leverages the cutting edge of machine learning and predictive technology to guide our clients on where to purchase investment properties or their retirement homes.


# For Users -- General Overview & Flow

Part 1: Data inputs will be generated to determine the years in retirement, size and risk profile of the user's investment portfolio, and historical growth rates of indices.    

Part 2: Users will forecast the performance of their portfolio at the age they wish to retire until the time they choose to retire. Historical price data will be used to generate Monte Carlo simulations to compute total savings (mean) for the time, which elapses btwn the user's current age and the year they prefer to retire.

Part 3: This total cash savings, in addition to asset appreciation will be exported to the Cost of Living Calculator to determine the list of viable cities where the user can retire.

# List of Cities within Scope of Analysis
Hamilton (Bermuda)
<br>
Hong Kong
<br>
Los Angeles
<br>
Paris
<br>
Milan
<br>
Bucaramanga (Colombia)
<br>
Mardrid
<br>
Delhi
<br>
Hamilton (Canada)


---

# Documents

###Team Presentation (Slides)
<br>
https://docs.google.com/presentation/d/1telx0y47zEFE7gah3XCnOr20Z_wnIJqP7ymZ5ulgjtM/edit?usp=sharing


###Team Charter
<br>
https://docs.google.com/document/d/1laAHUYkqxnocPBQqIeRB0HaU6wA8JShfNR4nlD4YaIU/edit?usp=sharing

---

## Technologies

Required programs, libraries, systems, and overall dependencies:
<br>
Python (version 3.0 or later)
<br>
`Amazon Lex == V2`
<br>
`Pathlib`
<br>
`pandas`
<br>
`%matplotlib`
<br>
`hvplot.pandas`
<br>
`sqlalchemy`
<br>
`numpy`
<br>
`simulation`
<br>
`fileio`
<br>
`fire==0.4.0`
<br>
pip==22.0.4
<br>
prompt-toolkit==3.0.28
<br>
questionary==1.10.0
<br>
setuptools==58.1.0
<br>
six==1.16.0
<br>
termcolor==1.1.0
<br>
wcwidth==0.2.5
<br>
wheel==0.37.1
<br>
---

## Installation Guide

`pip install Voila`
<br>
`pip install Fire`
<br>
`pip install folium`
<br>
`conda install -c pyviz hvplot geoviews`

---

## Usage of Retirement Global 2.0 App

Getting User info:

```python
import questionary
def get_retire_plan_user():
    age = questionary.text("What is your current age").ask()
    retirement_age = questionary.text("By what age, would you prefer to retire?").ask()
    savings = questionary.text("How much do you have in liquid cash savings (USD)").ask()
    portfolio_type = questionary.text("Would you like your portfolio to be conservative[1], conservatively moderate[2], or moderate[3]? (Enter 1, 2, or 3)").ask()
    total_stocks_bonds = questionary.text("How much would you like to invest in stocks and bonds?").ask()
        
    age = int(age)
    retirement_age = int(retirement_age)
    savings = float(savings)
    portfolio_type = int(portfolio_type)
    total_stocks_bonds = float(total_stocks_bonds)
    return age, retirement_age, savings, portfolio_type, total_stocks_bonds
```

Snippet of Monte Carlo code

```python
output = simulation.run_mc_output(df_portfolio, portfolio_type, years_to_retirement)
output
output.calc_cumulative_return()
```

## View of Amazon Lex Screen
![view_Lex_screen](https://user-images.githubusercontent.com/11021924/168452484-30cb0b8b-74b0-4a17-b8da-7570feaa83e8.png)

## Short Clip of Amazon Lex Chatbot
![view_Lex_screen](https://user-images.githubusercontent.com/11021924/168452484-30cb0b8b-74b0-4a17-b8da-7570feaa83e8.png)

## Forecast Simulation
![sample_output_MC](https://user-images.githubusercontent.com/11021924/168452488-f5470627-b15b-4166-8dd5-ace160e4e9c0.png)


---

# Useful GitHub commands for Group Coordination

`git checkout -b [BRANCH_NAME]`: new branch

`git checkout [BRANCH_NAME]`: change branch

`git branch` : which branch am I in

when i wanna push code:
<br>
`git add -A` / `git add filename`
<br>
`git commit -m "COMMIT_MESSAGE"`
<br>
`git push`
if this doesn’t work
`git pull --rebase origin master` then try `git push` again

`git branch -D {BRANCH_NAME}` delete branch

---

## Contributors

Tracy Davis
<br>
Reginald Hyppolite
<br>
Jesse Lee
<br>
Wonkyung Lee
<br>
Tyler Shubert

BIG THANKS to all the great TAs and Professor Vinicio DeSola

---

## License
MIT