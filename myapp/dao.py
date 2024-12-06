import json

def load_categories():
    try:
        with open("data/categories.json", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("File categories.json not found!")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON from categories.json!")
        return []

def load_products(q=None, cate_id=None):
    try:
        with open("data/products.json", encoding="utf-8") as f:
            products = json.load(f)

            if q:
                products = [p for p in products if q.lower() in p["name"].lower()]  # Tìm kiếm không phân biệt hoa thường
            if cate_id:
                products = [p for p in products if p["category_id"] == int(cate_id)]

            return products
    except FileNotFoundError:
        print("File products.json not found!")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON from products.json!")
        return []

def load_product_by_id(id):
    try:
        with open('data/products.json', encoding='utf-8') as f:
            products = json.load(f)
            for p in products:
                if p["id"] == id:
                    return p
            return None  # Trả về None nếu không tìm thấy sản phẩm
    except FileNotFoundError:
        print("File products.json not found!")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON from products.json!")
        return None

if __name__ == "__main__":
    products = load_products(q="shirt", cate_id=2)  # Tìm sản phẩm có tên chứa "shirt" và thuộc category_id = 2
    for product in products:
        print(product)
