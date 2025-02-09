import sys
import time
import json

# Constants
SALES_RESULTS_FILE = "SalesResults.txt"


def read_json_file(file_name):
    """Reads a JSON file and returns its content."""
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' does not exist.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: The file '{file_name}' is not a valid JSON.")
        sys.exit(1)


def get_product_prices(product_file):
    """Gets product prices from a JSON file."""
    products = read_json_file(product_file)
    product_prices = {}
    for product in products:
        product_prices[product["title"]] = product["price"]
    return product_prices


def get_sales(sales_file):
    """Gets sales data from a JSON file."""
    return read_json_file(sales_file)


def calculate_total_cost(product_prices, sales):
    """Calculates the total cost of sales."""
    total_cost = 0
    for sale in sales:
        try:
            product_price = product_prices[sale["Product"]]
            quantity = int(sale["Quantity"])
            total_cost += product_price * quantity
        except KeyError:
            print(f"""Error: Product '{sale['Product']}'
            not found in price catalog.""")
    return total_cost


def write_results_to_file(results):
    """Writes results to a file."""
    try:
        with open(SALES_RESULTS_FILE, "w", encoding="utf-8") as file:
            file.write("\n".join(results) + "\n")
    except IOError as error:
        print(f"Error writing to file: {error}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("""Usage:
        python computeSales.py priceCatalogue.json salesRecord.json""")
        sys.exit(1)

    price_file = sys.argv[1]
    sales_file = sys.argv[2]

    start_time = time.time()

    product_prices = get_product_prices(price_file)
    sales = get_sales(sales_file)
    total_cost = calculate_total_cost(product_prices, sales)

    print(f"Total cost: {total_cost:.2f}")

    elapsed_time = time.time() - start_time
    execution_time = f"Execution time: {elapsed_time:.4f} seconds"

    results = [f"Total cost: {total_cost:.2f}", execution_time]
    write_results_to_file(results)

    print(execution_time)
