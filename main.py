import matplotlib.pyplot as plt
import numpy as np


def menu():
    print('''\nWelcome to Simply Screws!
Here are our services:
1. View screw types available
2. View total units in stock in each length category
3. View screws by selected length category
4. Query screw category and increase/decrease stock
5. Apply 10% discount
6. View bar chart, showing number of units per length category.
7. Exit
''')
    userChoice = input('Select an option (Enter 1, 2, 3, etc.): ')

    if userChoice == '1':
        show_available_stock(stock)
        
    elif userChoice == '2':
        show_units_by_length(stock)
        
    elif userChoice == '3':
        show_stock_by_length(stock)
        
    elif userChoice == '4':
        query_screw_category(stock)
        
    elif userChoice == '5':
        show_discount_prompt(stock)
        
    elif userChoice == '6':
        graph_units_by_length(stock)
        
    elif userChoice == '7':
        print('Exiting program...')
        return
    
    else:
        print('Invalid option entered, please try again')
        menu()


def get_stock():
    with open('data_file.txt', 'r') as f:
        stockFile = f.readlines()[2::] # Adding lines barring first and second to list
        
    stockList = []
    for item in stockFile:
        item = item.strip('\n') # Removing linebreak
        item = item.split(',') # Turning individual products into their own lists
        stockList.append(item) # Putting into masterlist.

    return stockList


def show_available_stock(stock):
    
    totalUnits, totalValue = 0, 0
    
    for item in stock: # Iterating through products, each line being a different product.
        print(f'Material: {item[0]} \t Head Type: {item[1]} \t Length: {item[2]} \t Boxes (50): {item[3]}  \t Boxes (100): {item[4]} \t Boxes (200): {item[5]} \t Cost per 50 (£): {item[6]}')

        totalUnits += int(item[3]) * 50 # boxes of 50
        totalValue += calc_price('50', int(item[3]), float(item[6]))
        totalUnits += int(item[4]) * 100 # boxes of 100
        totalValue += calc_price('100', int(item[4]), float(item[6])) 
        totalUnits += int(item[5]) * 200 # boxes of 200
        totalValue += calc_price('200', int(item[5]), float(item[6])) 
        
        
    print(f'The total number of units in stock: {totalUnits}')
    print(f'The total value of the stock: £{totalValue}')
    
    menu()


def get_units_by_length(stock):
    len20Units, len40Units, len60Units = 0, 0, 0 
    
    for item in stock:
        if int(item[2]) == 20: # If length is 20, add to len20Units
            len20Units += int(item[3]) * 50
            len20Units += int(item[4]) * 100
            len20Units += int(item[5]) * 200
            
        elif int(item[2]) == 40: # If length is 40, add to len40Units
            len40Units += int(item[3]) * 50
            len40Units += int(item[4]) * 100
            len40Units += int(item[5]) * 200
            
        elif int(item[2]) == 60: # If length is 60, add to len60Units
            len60Units += int(item[3]) * 50
            len60Units += int(item[4]) * 100
            len60Units += int(item[5]) * 200
    
    units = [len20Units, len40Units, len60Units] # List to be returned
    
    return units


def show_units_by_length(stock):
    
    unitsByLength = get_units_by_length(stock) # create list of total units by length category
    
    print(f'Total units in length 20: {unitsByLength[0]}\nTotal units in length 40: {unitsByLength[1]}\nTotal units in length 60: {unitsByLength[2]}')
    
    menu()
    
    
def show_stock_by_length(stock):  
    try:
        inputtedLength = int(input('Enter length to search for (20, 40, 60): '))
        
        # If inputtedLength is valid, run this
        if inputtedLength in [20, 40, 60]: 
            for item in stock:
                # compare screw information, print if match
                if int(item[2]) == inputtedLength: 
                    print(f'Material: {item[0]} \t Head Type: {item[1]} \t Length: {item[2]} \t Boxes (50): {item[3]}  \t Boxes (100): {item[4]} \t Boxes (200): {item[5]} \t Cost per 50 (£): {item[6]}')
        
        else: # If inputtedLength is NOT valid, run this
            print('Invalid option entered, returning to menu')
            
    except: # Run if input cant be converted to int (i.e. string is entered)
        print('Invalid option entered, returning to menu')
        
    menu()
    
    
def query_screw_category(stock):

    screwMaterial = input('Enter screw material: ').lower() 
    # Using .lower() to prevent case sensitivity issues
    headType = input('Enter head type: ').lower()
    screwLength = input('Enter screw length: ')
    
    screwExists = False # Boolean value for checking if screw exists
    
    for item in stock:
        # If user inputted details matches a screw in stock, screwExists is True
        if (item[0] == screwMaterial) and (item[1] == headType) and (item[2] == screwLength):
            screwExists = True 

    if screwExists: # If screw exists in stock, run this code
        print('Screw category exists')
        print('''Would you like to either:
1. Increase stock level
2. Decrease Stock level
3. Cancel''')
        userChoice = input('Select an option (1, 2): ')
        
        if userChoice == '1': # selects increase stock level
            # Calling increaseStock function and passing screw information
            increase_stock(stock, screwMaterial, headType, screwLength) 
            
        elif userChoice == '2': # selects decrease stock level
            # Calling decreaseStock function and passing screw information
            decrease_stock(stock, screwMaterial, headType, screwLength) 
        
        elif userChoice == '3': # selects cancel
            print('Cancelling and returning to menu...')
            menu()
            
        else: # if something NOT 1, 2 or 3 is inputted, run
            print('Invalid option entered, returning to menu')
            menu()
            
    else: # if screw can't be found, run this code
        print('Screw category does not exist, returning to menu')
        menu()
        
        
def increase_stock(stock, material, type_, length):
    for item in stock:
        if (item[0] == material) and (item[1] == type_) and (item[2] == length): # Find correct screw category
            print('Original screw information') # Print screw category pre-changes
            print(f'Material: {item[0]} \t Head Type: {item[1]} \t Length: {item[2]} \t Boxes (50): {item[3]}  \t Boxes (100): {item[4]} \t Boxes (200): {item[5]} \t Cost per 50 (£): {item[6]}')
    
            boxChosen = input('Select box to edit (50, 100, 200): ')
            if boxChosen not in ['50', '100', '200']:
                print('Invalid option entered, returning to menu')
                menu()
                
            unitIncrease = int(input('Enter units to increase by: '))
            
            # Change stock level based on box type and unit increase
            if boxChosen == '50':
                item[3] = int(item[3]) + unitIncrease
                
            elif boxChosen == '100':
                item[4] = int(item[4]) + unitIncrease
                
            elif boxChosen == '200':
                item[5] = int(item[5]) + unitIncrease
            
            
            print('Updated screw information') # Print screw category post-changes
            print(f'Material: {item[0]} \t Head Type: {item[1]} \t Length: {item[2]} \t Boxes (50): {item[3]}  \t Boxes (100): {item[4]} \t Boxes (200): {item[5]} \t Cost per 50 (£): {item[6]}')
            
            menu()
                    
def decrease_stock(stock, material, type_, length):
    tenPercentDiscount = False
    
    for item in stock:
        if (item[0] == material) and (item[1] == type_) and (item[2] == length): # Find correct screw category
            print('Original screw information') # Print screw category pre-changes
            print(f'Material: {item[0]} \t Head Type: {item[1]} \t Length: {item[2]} \t Boxes (50): {item[3]}  \t Boxes (100): {item[4]} \t Boxes (200): {item[5]} \t Cost per 50 (£): {item[6]}')
            
            boxChosen = input('Select box to edit (50, 100, 200): ')
            try: 
                unitDecrease = int(input('Enter units to decrease by: '))
            except: 
                print('Invalid option provided, returning to menu')
                menu()
                
            if item[7] == ' yes':
                tenPercentDiscount = True
                print('Discounted item, applying 10% discount.')
            
            # Changes stock level depending on box type chosen and unit decrease determined
            if boxChosen == '50':
                item[3] = int(item[3]) - unitDecrease # Decrease stock level accordingly
                partial_order(item[3], unitDecrease, float(item[6]), tenPercentDiscount, boxChosen) # Check if order can be 100% fulfilled
                    
            elif boxChosen == '100':
                item[4] = int(item[4]) - unitDecrease
                partial_order(item[4], unitDecrease, float(item[6]), tenPercentDiscount, boxChosen)
                    
            elif boxChosen == '200':
                item[5] = int(item[5]) - unitDecrease
                partial_order(item[5], unitDecrease, float(item[6]), tenPercentDiscount, boxChosen)
                
                
            if boxChosen == '50' and item[3] < 0:
                item[3] = 0
            elif boxChosen == '100' and item[4] < 0:
                item[4] = 0
            elif boxChosen == '200' and item[5] < 0:
                item[5] = 0
            
            print('Updated screw information') # Print screw category post-changes 
            print(f'Material: {item[0]} \t Head Type: {item[1]} \t Length: {item[2]} \t Boxes (50): {item[3]}  \t Boxes (100): {item[4]} \t Boxes (200): {item[5]} \t Cost per 50 (£): {item[6]}')
            
            menu()


def partial_order(box, decrease, price, tenPercentDiscount, boxType):
    
    if box < 0: # If order can only be partially fulfilled, run this code
        print('This order can only be partially fulfilled.')
        userChoice = input('Do you wish to continue? (Y/N) ').lower() # Avoiding case sensitivity errors using .lower()
        
        if userChoice == 'y' or userChoice == 'yes': # If user selects y/yes, run this code
            unitsPurchased = box + decrease # Calculates how many units can be fulfilled
            totalCost = calc_price(boxType, unitsPurchased, price, tenPercentDiscount)
            print(f'You will be purchasing {unitsPurchased}.')
            print(f"The total cost will be £{format(totalCost, '.2f')}")
            

        if userChoice == 'n' or userChoice == 'no': # If user selects n/no, run this code
            print('User stopped purchase, returning to menu')
            
        else: # If user enters something that is NOT y, yes, n, or no, run this code
            print('Invalid option provided, returning to menu')
            
    else: # If order can be 100% fulfilled, run this code
        totalCost = calc_price(boxType, decrease, price, tenPercentDiscount)
        print(f'You will be purchasing {decrease} units.')
        print(f"The total cost will be £{format(totalCost, '.2f')}")
    

def get_highest_stock(stock): 
    
    highestQuantity = 0 # Create variable to store highest quantity
    
    for item in stock:
        itemQuantity = 0 # Create temp variable to store quantity of current item
        itemQuantity += int(item[3]) * 50 # Units from boxes of 50
        itemQuantity += int(item[4]) * 100 # Units from boxes of 100
        itemQuantity += int(item[5]) * 200 # Units from boxes of 200
        
        if itemQuantity > highestQuantity: # If current item is higher than previous highest quantity, run this code
            highestQuantity = itemQuantity # Sets new highest quantity
            highestStock = [item[0], item[1], item[2]] # Stores screw category information in list

    return highestStock # Returns list containing screw category information


def get_current_discount(stock): 
    discount = False
    
    for item in stock: 
        if item[7] == ' yes': # If item has a discount create list storing its screw category information
            currentDiscount = [item[0], item[1], item[2]]
            discount = True # Discount already present, sets boolean value to True
            
    if discount == True: # If discount already exists, run this code
        return currentDiscount
    
    elif discount == False: # If no discount exists, run this code
        return False


def change_discount(stock, screwCategory): 
    for item in stock: # Go through each item, if it has discount applied, set column to no
        if item[7] == ' yes': 
            item[7] == ' no'
        
    for item in stock: # Go through each item, find newly discounted item, set column to yes
        if item[0] == screwCategory[0] and item[1] == screwCategory[1] and item[2] == screwCategory[2]:
            item[7] == ' yes'
    
    menu()
            
            
def show_discount_prompt(stock): 
    existingDiscount = False
    highestStock = get_highest_stock(stock)
    
    if get_current_discount(stock) != False: # If there IS an existing discount, run this code
        currentDiscount = get_current_discount(stock) # Create list storing current discount screw category information
        existingDiscount = True
        
    else: # If there is NOT an existing discount, run this code
        existingDiscount = False

    # Show screw category with highest stock
    print(f'Material: {highestStock[0]} Head Type: {highestStock[1]} Length: {highestStock[2]} currently has the highest stock.')
    
    discountChoice = input('Would you like to place a 10% discount on this category? (Y/N) ').lower() # Removing case sensitivity with .lower()
    
    if discountChoice == 'y' or discountChoice == 'yes': # If user enters y/yes, run this code
        if existingDiscount == True: # If there is already a discount running, show screw category and ask if user wants to overwrite it
            print(f'Material: {currentDiscount[0]} Head Type: {currentDiscount[1]} Length: {currentDiscount[2]} already has a discount running.')
            overwriteChoice = input('Would you like to overwrite this discount? (Y/N) ')
            
            if overwriteChoice == 'y' or overwriteChoice == 'yes': # If user wants to overwrite discount, run this code
                print('New discount applied')
                change_discount(stock, highestStock)
                
            if overwriteChoice == 'n' or overwriteChoice == 'no': # If user does not want to overwrite discount, run this
                print('Not applying discount')
                
        else: # If there is no other discount running, run this code
            print('Applying 10% discount.')
            change_discount(stock, highestStock)
            
                
    elif discountChoice == 'n' or discountChoice == 'no': # if user enters n/no, run this code
        print('Not applying discount')
        
    else:
        print('Invalid option entered, returning to menu')

    menu()


def calc_price(boxType, unitsPurchased, unitPrice, tenPercentDiscount=False): # tenPercentDiscount is set to false by default
    box100Discount = 0.9 # Discount on boxes of 100
    box200Discount = 0.85 # Discount on boxes of 200
    
    if boxType == '50':
        price = unitsPurchased * unitPrice # Price is number of units purchased by price of each unit
        
    elif boxType == '100':
        price = unitsPurchased * unitPrice
        price *= 2 # unitPrice is per box of 50, so must multiply by 2 to get 100
        price *= box100Discount
        
    elif boxType == '200':
        price = unitsPurchased * unitPrice
        price *= 4 #  unitPrice is per box of 50, so must multiply by 4 to get 200
        price *= box200Discount
    
    if tenPercentDiscount == True: # if the 10% discount is applied, reduce price
        price *= 0.9
    
    return price


def graph_units_by_length(stock):
    y = np.array(get_units_by_length(stock)) # Get total units by length category as numpy array
    x = np.array(['20', '40', '60']) # X axis names
    
    plt.bar(x,y) # Creating bar chart
    
    plt.title('Total units per length category', loc = 'left') # Adding title at top left
    plt.ylabel('Total Units') # Labeling y axis
    plt.xlabel('Length Category') # Labeling x axis
    
    plt.show() # Showing graph
    
    menu()


if __name__ == '__main__': # On program start
    stock = get_stock() 
    menu()
    
    
# 401 Lines
# 17 Functions