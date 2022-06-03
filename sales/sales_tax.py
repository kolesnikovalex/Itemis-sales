import re
import math


class SalesTax:
    reg_ex = r'^\d+\s([A-Za-z]+\s?)+\sat\s[0-9]{1,6}[.,]\d{1,2}'
    price_reg_ex = r'^\d{1,6}[.,]\d{1,2}'
    str_template = '''
    "product value - integer" "name of product" "at" "product price - float"
    correct row example
    1 book at 12.49
    '''
    tax_free = ('book', 'pills', 'chocolate')
    products = []

    @classmethod
    def check_product_value(cls, value: str):
        try:
            value = int(value)
        except ValueError:
            raise ValueError('product value could not convert to float')
        if value == 0:
            raise ValueError('product value could be 0')
        return value

    @classmethod
    def check_product_price(cls, price: str):
        if not re.fullmatch(cls.price_reg_ex, price):
            raise ValueError('price uncorrect')
        else:
            try:
                price = float(price)
            except ValueError:
                raise ValueError('price could not convert to float')
        return price

    def parse_row(self, row: str) -> dict or None:
        value, row = row.split(' ', 1)
        row_split = row.split(' at ')
        price = row_split.pop(-1)
        name = ' '.join(row_split)
        imported = True if "imported" in name else False
        price = self.check_product_price(price)
        value = self.check_product_value(value)
        name = name.replace('imported', '').strip()
        product = {
            "value": value,
            "price": price,
            "tax": 10 if not imported else 15,
            "name": name,
            "tax_free": any(i in name for i in self.tax_free),
            "total": 0
        }
        if product["tax_free"]:
            if imported:
                product["tax"] = 5
            else:
                product["tax"] = 0
        return product

    def calculate_receipt(self):
        total = 0
        tax = 0
        response = ''
        for product in self.products:
            if product["tax"] == 0:
                taxes = 0
            else:
                t = product["value"] * product["price"] * product["tax"] / 100
                if int(t * 100) % 5 != 0:
                    tx = math.floor((t - int(t)) * 100)
                    taxes = int(t) + (tx - tx % 5 + 5) / 100
                else:
                    taxes = t
            tax += taxes
            product["total"] = round(product["value"] * product["price"] + taxes, 2)
            total += product["total"]
            response += f'{product["value"]} {product["name"]}: {product["total"]}\n'
        tax = round(tax, 2)
        total = round(total, 2)
        response += f'Sales Taxes: {tax}\n'
        response += f'Total: {total}'
        print(response)

    def get_data(self):
        print("Hello, Input product row\nProduct example:", self.str_template)
        print("type exit to calculate and exit")
        while True:
            input_str = input().strip()
            if input_str == 'exit':
                break
            if len(input_str) > 0:
                if re.fullmatch(self.reg_ex, input_str):
                    self.products.append(self.parse_row(input_str))
                else:
                    print("input string not correct - ", input_str)

    def run(self):
        self.get_data()
        self.calculate_receipt()


if __name__ == '__main__':
    s = SalesTax()
    s.run()
