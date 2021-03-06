import redis


def generate_id():
    try:
        connect = connection()

        key = connect.get('key')

        if key:
            key = connect.incr('key')
            return key

        else:
            connect.set('key', 1)
            return 1
    except redis.exceptions.ConnectionError as e:
        print(f'It was not possible to generate the key: {e}')


def connection():
    """
    Function to connect to server
    """
    connect = redis.Redis(host='localhost', port=6379, db=13)

    return connect


def disconnection(connect):
    """
    Function to disconnect from server
    """
    connect.connection_pool.disconnect()


def list_products():
    """
    Function to list products
    """
    connect = connection()

    try:
        data = connect.keys(pattern='product:*')

        if len(data) > 0:
            print('Listing products...')
            print('-------------------')
            for key in data:
                product = connect.hgetall(key)
                print(f"ID: {str(key, 'utf-8', 'ignore')}")
                print(f"Country: {str(product[b'Country'], 'utf-8', 'ignore')}")
                print(f"Country Code: {str(product[b'Country Code'], 'utf-8', 'ignore')}")
                print(f"Number of homicides per 100,000: {str(product[b'Number of homicides per 100,000'], 'utf-8', 'ignore')}")
                print('-------------------')
        else:
            print('There are no products registred')
    except redis.exceptions.ConnectionError as e:
        print(f'It was not possible to list the products: {e}')

        disconnection(connect)

def show_country_details(country):
    """
    Function to list products
    """
    connect = connection()

    try:
        data = connect.keys(pattern=f'{country}')

        if len(data) > 0:
            print('Getting Country...')
            print('-------------------')
            for key in data:
                fetched = connect.hgetall(key)
                print(f"ID: {str(key, 'utf-8', 'ignore')}")
                print(f"Country: {str(fetched[b'Country'], 'utf-8', 'ignore')}")
                print(f"Country Code: {str(fetched[b'Country Code'], 'utf-8', 'ignore')}")
                print(f"Number of homicides per 100,000: {str(fetched[b'Number of homicides per 100,000'], 'utf-8', 'ignore')}")
                print('-------------------')
        else:
            print('There are no products registred')
    except redis.exceptions.ConnectionError as e:
        print(f'It was not possible to list the products: {e}')

        disconnection(connect)



def insert_product():
    """
    Function to insert a product
    """
    connect = connection()

    name = input('Country: ')
    price = float(input('Number of homicides per 100,000: '))
    stash = str(input('Country Code: '))

    product = {'Country': name, 'Number of homicides per 100,000': price, 'Country Code': stash}
    key = f'product:{generate_id()}'

    try:
        answer = connect.hmset(key, product)

        if answer:
            print(f'The product {name} was successfully inserted.')
        else:
            print(f'It was not possible to insert the product')
    except redis.exceptions.ConnectionError as e:
        print(f'It was not possible to insert the product: {e}')

        disconnection(connect)


def update_product():
    """
    Function to update a product
    """
    connect = connection()

    old_given_name = input('Provide product name to update: ')

    name = input('Provide product new/updated name: ')
    price = float(input('Provide product new/updated Number of homicides per 100,000: '))
    stash = int(input('Provide new/updated Country Code: '))

    new_product = {'Country': name, 'Number of homicides per 100,000': price, 'Country Code': stash}
    try:
        data = connect.keys(pattern='product:*')

        match_flag = 0

        for key in data:
            product = connect.hgetall(key)
            old_database_name = str(product[b'product'], 'utf-8', 'ignore')

            if old_database_name == old_given_name:
                key_string = key.decode('utf-8')
                updating = connect.hmset(key_string, new_product)
                print(key_string, product)
                print(f'The product {old_given_name} was successfully updated')
                match_flag += 1

            else:
                pass

        if match_flag == 0:
            print(f'There is no product {old_given_name} in database to be updated!')

    except redis.exceptions.ConnectionError as e:
        print(f'It was not possible to update the product: {e}')

        disconnection(connect)


def delete_product():
    """
    Function to delete product
    """
    connect = connection()

    key = input('Provide product key: ')

    try:
        result = connect.delete(key)

        if result == 1:
            print('Product deleted')
        else:
            print('There is no product with this key')
    except redis.exceptions.ConnectionError as e:
        print(f'Error connecting to Redis: {e}')
        disconnection(connect)


def menu():
    """
    Function to generate main menu
    """
    while True:
        print('\nMENU\n')
        print('1) List values')
        print('2) Insert value')
        print('3) Update value')
        print('4) Delete value')
        print('5) Exit')
        print('\n')

        try:
            option = int(input('Choose an option: '))

            if option == 1:
                list_products()
            elif option == 2:
                insert_product()
            elif option == 3:
                update_product()
            elif option == 4:
                delete_product()
            elif option == 6:
                show_country_details(input("Enter Country short code:"))
            elif option == 5:
                print('Exiting...')
                break
            else:
                print('Option not found, try again')
        except ValueError:
            print('Option not found, try again')

if __name__ == '__main__':
    menu()