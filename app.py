from flask import Flask
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.get('/products')
def getProducts():
    result = cursor.execute('''SELECT * FROM products''')
    data = result.fetchall()
    conn.commit()

    product_list = []

    for item in data:
        product_list.append(
            {
                "id": item[0],
                "title": item[1],
                "price": item[5],
                "description": item[3],
                "category": item[2],
                "image": item[4],
                "rating": {
                    "rate": 3.9,
                    "count": 120
                }
            }
        )

    return product_list

@app.get('/products/<int:product_id>')
def get_product_by_id(product_id: int):
    result = cursor.execute('''SELECT * FROM products WHERE id = ?''', (product_id,))
    data = result.fetchone()
    conn.commit()

    if data is None:
        return {"error": "Product not found"}

    product = {
        "id": data[0],
        "title": data[1],
        "price": data[5],
        "description": data[3],
        "category": data[2],
        "image": data[4],
        "rating": {
            "rate": 3.9,
            "count": 120
        }
    }

    return product


if __name__ == '__main__':
    app.run()
