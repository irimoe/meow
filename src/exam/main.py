import pandas as pd
import os
from datetime import datetime

class Colours: 
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

class MainMenuChoice:
    AVERAGE_INTERACTION = "1"
    EXIT = "0"

class AverageMenuChoice:
    LIKES = "1"
    SHARES = "2"
    COMMENTS = "3"
    BACK = "0"
 

##################################################################
# display and user interactions
##################################################################

def display_header(title):
    clear_screen()
    print("#" * 50)
    print(f"{'# ' + title + ' #':^50}")
    print("#" * 50)
    print("")

def get_validated_input(prompt, valid_options):
    attempts = 0
    current_prompt = prompt
    while True:
        choice = -1
        if attempts > 0: choice = input(f" x {current_prompt}: ").strip()
        else: choice = input(f" | {current_prompt}: ").strip()
        
        if choice in valid_options:
            return choice
        
        error_msg = f"{Colours.RED}invalid option! please select from: {', '.join(valid_options)}{Colours.RESET} •"
        current_prompt = f"{error_msg} {prompt}"
        attempts += 1


##################################################################
# menus 
##################################################################

def main_menu():
    display_header("snowy animal rescue")
    
    print("please select an option:")
    print(" 1. average social media interaction data")
    print(" 0. exit program")
    print("")
    
    return get_validated_input("enter your selection here", 
                               [MainMenuChoice.AVERAGE_INTERACTION, 
                                MainMenuChoice.EXIT])

def average_menu():
    display_header("average interactions")
    
    print("please select an option:")
    print(" 1. average number of likes")   
    print(" 2. average number of shares") 
    print(" 3. average number of comments")
    print(" 0. back to main menu")
    print("")
    
    return get_validated_input("enter your selection here", 
                             [AverageMenuChoice.LIKES, 
                              AverageMenuChoice.SHARES, 
                              AverageMenuChoice.COMMENTS,
                              AverageMenuChoice.BACK])


##################################################################
# utility functions
##################################################################

# converts the average menu choice to the relevant column name in the 
# dataframe.
def convert_avg_menu_choice(avg_menu_choice):
    choice_mapping = {
        AverageMenuChoice.LIKES: "Likes",
        AverageMenuChoice.SHARES: "Shares",
        AverageMenuChoice.COMMENTS: "Comments"
    }
    mapping = choice_mapping.get(avg_menu_choice, "unknown")
    if mapping == "unknown":
        raise ValueError(f"invalid average menu choice: {avg_menu_choice}")
    return mapping

def clear_screen():
    # if the user is on a unix-like system, use `clear`. otherwise, use `cls`
    os.system('cls' if os.name == 'nt' else 'clear')
    

##################################################################
# data loading and processing
##################################################################

def load_data(filename="data.csv"):
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        print(f"{Colours.RED}error: file '{filename}' not found.{Colours.RESET}")
        return None
    except pd.errors.EmptyDataError:
        print(f"{Colours.RED}error: file '{filename}' is empty.{Colours.RESET}")
        return None
    except pd.errors.ParserError:
        print(f"{Colours.RED}error: unable to parse '{filename}'.{Colours.RESET}")
        return None

def get_avg_data(avg_choice, df=None):
    if df is None:
        df = load_data()
        
    if df is None:
        return f"{Colours.RED}error: no data available.{Colours.RESET}"
    
    try:
        extract = df.groupby(['Date'], as_index=False)[avg_choice].mean()
        
        result = f"average number of {avg_choice} each day during the campaign:\n"
        result += "-" * 45 + "\n"
        result += f"{'Date':<12} | {avg_choice:>10}\n"
        result += "-" * 45 + "\n"
        
        for _, row in extract.iterrows():
            result += f"{row['Date']:<12} | {row[avg_choice]:>10.2f}\n"
            
        result += "-" * 45 + "\n"
        result += f"overall average: {df[avg_choice].mean():.2f}\n"
        
        return result
    except KeyError:
        return f"{Colours.RED}error: column '{avg_choice}' wasn't found in the dataset.{Colours.RESET}"


##################################################################
# main function
##################################################################

def main():

    df = load_data()
    if df is None:
        print("couldn't load the date. exiting.")
        return
        
    while True:
        main_menu_choice = main_menu()
        
        if main_menu_choice == MainMenuChoice.EXIT:
            print(" • exiting, goodbye!")
            break
            
        elif main_menu_choice == MainMenuChoice.AVERAGE_INTERACTION:
            while True:
                avg_menu_choice = average_menu()
                
                if avg_menu_choice == AverageMenuChoice.BACK:
                    break
                    
                avg_column = convert_avg_menu_choice(avg_menu_choice)
                result = get_avg_data(avg_column, df)
                
                print("\n" + result)
                input(f"\npress {Colours.GREEN}Enter{Colours.RESET} to continue...")

if __name__ == "__main__":
    main()
