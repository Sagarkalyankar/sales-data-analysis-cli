import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns


sales_data = pd.read_csv("../PROJECT_DS/sales_data_sample.csv", encoding="latin-1")

def preview_data():
    print("Data Preview:")
    print(sales_data.head())

def check_missing_values():
    print("\nMissing Values:")
    print(sales_data.isnull().sum())

def handle_missing_values():
    sales_data.fillna(method='ffill', inplace=True)
    sales_data['ORDERDATE'] = pd.to_datetime(sales_data['ORDERDATE'], errors='coerce')
    sales_data.dropna(subset=['ORDERDATE'], inplace=True)

def sales_by_region():
    total_sales_by_region = sales_data.groupby('COUNTRY')['PRICEEACH'].sum()
    print("\nTotal Sales by Region:")
    print(total_sales_by_region)
    return total_sales_by_region

def avg_sales_by_product():
    avg_sales = sales_data.groupby('PRODUCTLINE')['PRICEEACH'].mean()
    print("\nAverage Sales by Product Line:")
    print(avg_sales)
    return avg_sales

def best_selling_product():
    best_selling = sales_data.loc[sales_data.groupby('COUNTRY')['PRICEEACH'].idxmax(), ['COUNTRY', 'PRODUCTLINE']]
    print("\nBest-Selling Product by Region:")
    print(best_selling)
    return best_selling

def monthly_sales_trend():
    if not np.issubdtype(sales_data['ORDERDATE'].dtype, np.datetime64):
        sales_data['ORDERDATE'] = pd.to_datetime(sales_data['ORDERDATE'], errors='coerce')
        sales_data.dropna(subset=['ORDERDATE'], inplace=True)    
        
    sales_data['MONTH'] = sales_data['ORDERDATE'].dt.month
    monthly_sales = sales_data.groupby('MONTH')['PRICEEACH'].sum()
    return monthly_sales

def product_line_distribution():
    product_line_sales = sales_data.groupby('PRODUCTLINE')['PRICEEACH'].sum()
    return product_line_sales

def plot_graphs():
    total_sales_by_region = sales_by_region()
    monthly_sales = monthly_sales_trend()
    product_line_sales = product_line_distribution()

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    axes[0, 0].bar(total_sales_by_region.index, total_sales_by_region.values, color='skyblue', edgecolor='black')
    axes[0, 0].set_title('Total Sales by Region')
    axes[0, 0].set_xlabel('Region')
    axes[0, 0].set_ylabel('Total Sales')
    axes[0, 0].tick_params(axis='x', rotation=45)

    
    sales_pivot = sales_data.pivot_table(index='COUNTRY', columns='PRODUCTLINE', values='PRICEEACH', aggfunc='sum')
    sns.heatmap(sales_pivot, annot=True, fmt='.1f', cmap='coolwarm', cbar_kws={'label': 'Sales'}, ax=axes[0, 1])
    axes[0, 1].set_title('Sales by Region and Product Line')
    axes[0, 1].set_xlabel('Product Line')
    axes[0, 1].set_ylabel('Region')

    
    axes[1, 0].plot(monthly_sales.index, monthly_sales.values, marker='o', color='green')
    axes[1, 0].set_title('Monthly Sales Trend')
    axes[1, 0].set_xlabel('Month')
    axes[1, 0].set_ylabel('Total Sales')
    axes[1, 0].grid(True)


    axes[1, 1].pie(product_line_sales, labels=product_line_sales.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
    axes[1, 1].set_title('Product Line Sales Distribution')

    plt.tight_layout()
    plt.show()

def main():
    while True:
        print("\nMenu:")
        print("1. Preview Data")
        print("2. Check Missing Values")
        print("3. Handle Missing Values")
        print("4. Display Sales by Region")
        print("5. Display Average Sales by Product Line")
        print("6. Display Best-Selling Product by Region")
        print("7. Display Graphs")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            preview_data()
        elif choice == '2':
            check_missing_values()
        elif choice == '3':
            handle_missing_values()
            print("Missing values handled.")
        elif choice == '4':
            sales_by_region()
        elif choice == '5':
            avg_sales_by_product()
        elif choice == '6':
            best_selling_product()
        elif choice == '7':
            plot_graphs()
        elif choice == '8':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

main()
