import matplotlib.pyplot as plt
import pandas as pd

from datetime import datetime
import random
import string
import os

class Colours: 
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"

class MainMenuChoice:
    ITEM_SALES = "1"
    MEAL_TRENDS = "2"
    TOP_ITEMS = "3"
    EXIT = "0"
 
class MealType:
    LUNCH = "Lunch"
    DINNER = "Dinner"

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

def get_date_range_input():
    while True:
        try:
            start_date = input(f" | enter start date (DD/MM/YYYY)   ").strip()
            start_datetime = datetime.strptime(start_date, '%d/%m/%Y')
            
            end_date = input(f" | enter end date (DD/MM/YYYY)     ").strip()
            end_datetime = datetime.strptime(end_date, '%d/%m/%Y')
            
            if end_datetime < start_datetime:
                print(f"{Colours.RED}   end date must be after the start date{Colours.RESET}")
                continue
                
            return start_date, end_date
            
        except ValueError:
            print(f"{Colours.RED}   invalid date format! use DD/MM/YYYY.{Colours.RESET}")

##################################################################
# menus 
##################################################################

def main_menu():
    display_header("Gurreb's BBQ Sales Analysis")
    
    print("please select an option:")
    print(" 1. sales data for specific menu item")
    print(" 2. lunch vs dinner trends")
    print(" 3. top selling menu items")
    print(" 0. exit program")
    print("")
    
    return get_validated_input("enter your selection here", 
                               [MainMenuChoice.ITEM_SALES,
                                MainMenuChoice.MEAL_TRENDS,
                                MainMenuChoice.TOP_ITEMS,
                                MainMenuChoice.EXIT])

def get_menu_items(df):
    menu_items = df['Menu Item'].unique().tolist()
    menu_item_map = {str(i+1): item for i, item in enumerate(menu_items)}
    
    display_header("select Menu Item")
    
    print("available menu items:")
    for key, item in menu_item_map.items():
        print(f" {key}. {item}")
    print(" 0. back to main menu")
    print("")
    
    valid_options = list(menu_item_map.keys()) + ["0"]
    choice = get_validated_input("enter your selection here", valid_options)
    
    if choice == "0":
        return None
    return menu_item_map[choice]

##################################################################
# utility functions
##################################################################

def clear_screen():
    # if the user is on a unix-like system, use `clear`. otherwise, use `cls`
    os.system('cls' if os.name == 'nt' else 'clear')
    
def generate_temp_filename():
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    if not os.path.exists("plots"): os.makedirs("plots")
    return f"plots/temp_plot_{random_str}.png"

def save_plot(plt, filename = None):
    if filename is None: filename = generate_temp_filename()

    plt.savefig(filename)
    return filename

##################################################################
# data loading and processing
##################################################################

def load_data(filename="Task4a_data.csv"):
    try:
        raw_df = pd.read_csv(filename, skiprows=0)
        
        meta_columns = ['Menu Item', 'Service']
        date_columns = [col for col in raw_df.columns if col not in meta_columns]
        
        melted_df = pd.melt(
            raw_df, 
            id_vars=meta_columns,
            value_vars=date_columns,
            var_name='Date',
            value_name='Quantity'
        )
        
        melted_df['Date'] = pd.to_datetime(melted_df['Date'], format='%d/%m/%Y', errors='coerce')
        melted_df.rename(columns={'Service': 'MealType'}, inplace=True)
        
        return melted_df
        
    except FileNotFoundError:
        print(f"{Colours.RED}error: file '{filename}' not found.{Colours.RESET}")
        return None
    except pd.errors.EmptyDataError:
        print(f"{Colours.RED}error: file '{filename}' is empty.{Colours.RESET}")
        return None
    except pd.errors.ParserError:
        print(f"{Colours.RED}error: unable to parse '{filename}'.{Colours.RESET}")
        return None
    except Exception as e:
        print(f"{Colours.RED}error: {str(e)}{Colours.RESET}")
        return None

##################################################################
# analysis
##################################################################

def analyze_item_sales(df, menu_item, start_date=None, end_date=None):
    try:
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%d/%m/%Y')
            end_date = datetime.strptime(end_date, '%d/%m/%Y')
            mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
            filtered_df = df[mask]
        else:
            filtered_df = df
        
        item_data = filtered_df[filtered_df['Menu Item'] == menu_item]
        if item_data.empty:
            return f"{Colours.RED}no sales data found for {menu_item} in the selected period.{Colours.RESET}", None
        
        daily_sales = item_data.groupby(item_data['Date'].dt.date)['Quantity'].sum().reset_index()
        daily_sales.columns = ['Date', 'Units Sold']
    
        plt.figure(figsize=(10, 5))
        plt.plot(daily_sales['Date'], daily_sales['Units Sold'], marker='o')
        plt.title(f"sales of {menu_item} over time")
        plt.xlabel('date')
        plt.ylabel('units sold')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
    
        plot_filename = save_plot(plt)
        plt.close()
    
        result = f"{Colours.GREEN}sales analysis for {menu_item}{Colours.RESET}\n"
        result += "-" * 50 + "\n"
        result += f"total units sold: {item_data['Quantity'].sum()}\n"
        result += f"average daily sales: {item_data.groupby(item_data['Date'].dt.date)['Quantity'].sum().mean():.2f} units\n"
        result += "-" * 50 + "\n"
        result += f"{'date':<12} | {'units sold':>10}\n"
        result += "-" * 50 + "\n"
        
        for _, row in daily_sales.iterrows():
            result += f"{row['Date'].strftime('%d/%m/%Y'):<12} | {row['Units Sold']:>10}\n"
        
        return result, plot_filename
    except Exception as e:
        return f"{Colours.RED}error analyzing item sales: {str(e)}{Colours.RESET}", None

def analyze_meal_trends(df, menu_item=None, start_date=None, end_date=None):
    try:
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%d/%m/%Y')
            end_date = datetime.strptime(end_date, '%d/%m/%Y')
            mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
            filtered_df = df[mask]
        else:
            filtered_df = df
        
        if menu_item:
            filtered_df = filtered_df[filtered_df['Menu Item'] == menu_item]
        
        if filtered_df.empty:
            return f"{Colours.RED}no sales data found for the selected criteria.{Colours.RESET}", None
        
        meal_trends = filtered_df.groupby([filtered_df['Date'].dt.date, 'MealType'])['Quantity'].sum().reset_index()
        pivot_df = meal_trends.pivot(index='Date', columns='MealType', values='Quantity').fillna(0)
        
        if MealType.LUNCH not in pivot_df.columns: pivot_df[MealType.LUNCH] = 0
        if MealType.DINNER not in pivot_df.columns: pivot_df[MealType.DINNER] = 0
        
        plt.figure(figsize=(12, 6))
        plt.plot(pivot_df.index, pivot_df[MealType.LUNCH], marker='o', label='Lunch', color='orange')
        plt.plot(pivot_df.index, pivot_df[MealType.DINNER], marker='s', label='Dinner', color='blue')
        
        title = 'lunch v. dinner sales trends'
        if menu_item:
            title += f' for {menu_item}'
            
        plt.title(title)
        plt.xlabel('date')
        plt.ylabel('units Sold')
        plt.grid(True)
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        plot_file = save_plot(plt)
        plt.close()
        
        lunch_total = filtered_df[filtered_df['MealType'] == MealType.LUNCH]['Quantity'].sum()
        dinner_total = filtered_df[filtered_df['MealType'] == MealType.DINNER]['Quantity'].sum()
        
        lunch_avg = filtered_df[filtered_df['MealType'] == MealType.LUNCH].groupby(filtered_df['Date'].dt.date)['Quantity'].sum().mean()
        dinner_avg = filtered_df[filtered_df['MealType'] == MealType.DINNER].groupby(filtered_df['Date'].dt.date)['Quantity'].sum().mean()
        
        report_title = 'lunch vs dinner comparison'
        if menu_item:
            report_title += f' for {menu_item}'
            
        result = f"{Colours.GREEN}{report_title}{Colours.RESET}\n"
        result += "-" * 50 + "\n"
        result += f"period: {min(pivot_df.index).strftime('%d/%m/%Y')} to {max(pivot_df.index).strftime('%d/%m/%Y')}\n"
        result += "-" * 50 + "\n"
        result += f"{'meal type':<12} | {'total sales':>10} | {'daily average':>15}\n"
        result += "-" * 50 + "\n"
        result += f"{'lunch':<12} | {lunch_total:>10.0f} | {lunch_avg:>15.2f}\n"
        result += f"{'dinner':<12} | {dinner_total:>10.0f} | {dinner_avg:>15.2f}\n"
        result += "-" * 50 + "\n"
        
        if lunch_total > dinner_total:
            result += f"{Colours.YELLOW}lunch service has higher total sales (+{lunch_total - dinner_total:.0f} units){Colours.RESET}\n"
            percentage = (lunch_total - dinner_total) / lunch_total * 100
            result += f"{Colours.YELLOW}                  +{percentage:.2f}% more sales than dinner{Colours.RESET}\n"
        elif dinner_total > lunch_total:
            result += f"{Colours.YELLOW}dinner service has higher total sales (+{dinner_total - lunch_total:.0f} units){Colours.RESET}\n"
            percentage = (dinner_total - lunch_total) / dinner_total * 100 
            result += f"{Colours.YELLOW}                   +{percentage:.2f}% more sales than lunch{Colours.RESET}\n"
        else:
            result += f"{Colours.YELLOW}lunch and dinner services have equal sales{Colours.RESET}\n"
        
        return result, plot_file
    except Exception as e:
        return f"{Colours.RED}error analysing meal trends: {str(e)}{Colours.RESET}", None

def find_top_items(df, start_date=None, end_date=None, limit=5):
    try:
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%d/%m/%Y')
            end_date = datetime.strptime(end_date, '%d/%m/%Y')
            mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
            filtered_df = df[mask]
        else:
            filtered_df = df
        
        if filtered_df.empty:
            return f"{Colours.RED}no sales data found for the selected period.{Colours.RESET}", None
        
        item_sales = filtered_df.groupby('Menu Item').agg({
            'Quantity': ['sum', 'mean'],
        }).reset_index()
        item_sales.head()
        
        item_sales.columns = ['Menu Item', 'TotalSales', 'AvgDailySales']
        top_by_quantity = item_sales.sort_values('TotalSales', ascending=False).head(limit)
        
        plt.figure(figsize=(10, 5))
        
        plt.bar(top_by_quantity['Menu Item'], top_by_quantity['TotalSales'], color='skyblue')
        plt.title('top items by quantity sold')
        plt.xlabel('menu item')
        plt.ylabel('total units sold')
        plt.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        plot_file = save_plot(plt)
        plt.close()
        
        result = f"{Colours.GREEN}top selling menu items analysis{Colours.RESET}\n"
        if start_date and end_date:
            result += f"period: {start_date.strftime('%d/%m/%Y')} to {end_date.strftime('%d/%m/%Y')}\n"
        result += "-" * 75 + "\n"
        result += f"{'menu item':<20} | {'total units':>10} | {'avg. daily':>10}\n"
        result += "-" * 75 + "\n"
        
        for _, row in top_by_quantity.head(limit).iterrows():
            result += f"{row['Menu Item']:<20} | {row['TotalSales']:>10.0f} | {row['AvgDailySales']:>10.2f}\n"
        
        result += "-" * 75 + "\n"
        result += f"{Colours.YELLOW}highest sales: {top_by_quantity.iloc[0]['Menu Item']} with {top_by_quantity.iloc[0]['TotalSales']:.0f} units{Colours.RESET}\n"
        
        return result, plot_file
    except Exception as e:
        return f"{Colours.RED}error finding top items: {str(e)}{Colours.RESET}", None

##################################################################
# main function
##################################################################

def main():
    df = load_data()
    if df is None:
        print("couldn't load the data. exiting.")
        return
        
    while True:
        main_menu_choice = main_menu()
        
        if main_menu_choice == MainMenuChoice.EXIT:
            print(" • exiting, goodbye!")
            break
            
        elif main_menu_choice == MainMenuChoice.ITEM_SALES:
            menu_item = get_menu_items(df)
            if menu_item is None:
                continue
            
            start_date, end_date = get_date_range_input()
            result, plot_file = analyze_item_sales(df, menu_item, start_date, end_date)
            
            print("\n" + result)
            if plot_file:
                print(f"\n{Colours.BLUE}a graph has been generated and saved as '{plot_file}'{Colours.RESET}")
            input(f"\npress {Colours.GREEN}Enter{Colours.RESET} to continue...")
            
            if plot_file and os.path.exists(plot_file):
                os.remove(plot_file)
                
        elif main_menu_choice == MainMenuChoice.MEAL_TRENDS:
            display_header("lunch v. dinner analysis")
            print("1. analyse specific menu item")
            print("2. analyse all items")
            print("0. back to main menu")
            
            choice = get_validated_input("enter your selection here", ["1", "2", "0"])
            
            if choice == "0":
                continue
                
            menu_item = None
            if choice == "1":
                menu_item = get_menu_items(df)
                if menu_item is None:
                    continue
                    
            start_date, end_date = get_date_range_input()
            result, plot_file = analyze_meal_trends(df, menu_item, start_date, end_date)
            
            print("\n" + result)
            if plot_file:
                print(f"\n{Colours.BLUE}a graph has been generated and saved as '{plot_file}'{Colours.RESET}")
            input(f"\npress {Colours.GREEN}Enter{Colours.RESET} to continue...")
            
            if plot_file and os.path.exists(plot_file):
                os.remove(plot_file)
                
        elif main_menu_choice == MainMenuChoice.TOP_ITEMS:
            display_header("top selling menu items")
            start_date, end_date = get_date_range_input()
            result, plot_file = find_top_items(df, start_date, end_date)
            
            print("\n" + result)
            if plot_file:
                print(f"\n{Colours.BLUE}a graph has been generated and saved as '{plot_file}'{Colours.RESET}")
            input(f"\npress {Colours.GREEN}Enter{Colours.RESET} to continue...")
            
            if plot_file and os.path.exists(plot_file):
                os.remove(plot_file)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print(f"\n{Colours.YELLOW}exiting, goodbye!{Colours.RESET}")
    except Exception as e: print(f"{Colours.RED}unexpected error: {str(e)}{Colours.RESET}")
        