import numpy as np
# EXPECTED INPUT
# items: string, string
# price: #.##, #.##
# Quantities: #, #
def process_resources(data):
    '''
    INPUT a dictionary with two values we care about, price and quantities
    OUTPUT a dictionary with a lot of maths applied to it
    Processes the resources input into a bunch of numbers we care about
    '''
    try:
        price = np.array(data['price'].split(','), dtype='float64')
        quantities = np.array(data['quantities'].split(','), dtype='int')

        count_price = len(price)
        count_quantities = len(quantities)

        sum_price = sum(price)
        sum_quantities = sum(quantities)

        min_price = min(price)
        min_quantities = min(quantities)

        max_price = max(price)
        max_quantities = max(quantities)

        mean_price = np.mean(price)
        mean_quantities = np.mean(quantities)

        std_price = np.std(price)
        std_quantities = np.std(quantities)

        mean_prices = sum_price / sum_quantities

        return {
            'count_price': count_price, 
            'count_quantities': count_quantities, 
            'sum_price': sum_price, 
            'sum_quantities': sum_quantities, 
            'min_price': min_price, 
            'min_quantities': min_quantities,
            'max_price': max_price,
            'max_quantities': max_quantities,
            'mean_price': mean_price,
            'mean_quantities': mean_quantities,
            'std_price': std_price,
            'std_quantities': std_quantities,
            'mean_prices': mean_prices
        }      
    except:
        return {
            'count_price': 0, 
            'count_quantities': 0, 
            'sum_price': 0, 
            'sum_quantities': 0, 
            'min_price': 0, 
            'min_quantities': 0,
            'max_price': 0,
            'max_quantities': 0,
            'mean_price': 0,
            'mean_quantities': 0,
            'std_price': 0,
            'std_quantities': 0,
            'mean_prices': 0
        }   