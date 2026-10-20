from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

products = []

class Product(BaseModel):
    id: int
    name: str
    price: float
    qty: int

#PRODUCT Create

@app.post("/product", status_code=status.HTTP_201_CREATED)
def create_product(product: Product):

    for existing_product in products:
        if existing_product["id"]== product.id:

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail= "Product Id Already Exists"
            )

    products.append(product.model_dump())

    return {"message": "Product Added Successfully",
            "product": product}

# PRODUCT READ
@app.get("/product")
def get_product():

    return products

# PRODUCT UPDATE

@app.put("/product/{product_id}", status_code=status.HTTP_200_OK)
def update_product(product_id: int, product: Product):

    for index, existing_product in enumerate(products):
        if existing_product["id"] == product_id:

            updated_product=product.model_dump()
            updated_product["id"] = product_id

            products[index] = updated_product
            

            return {"message": "Product Updated Succesfully",
                    "product": products[index]}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product Not Found"
    )

# PRODUCT deleted

@app.delete("/product/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(product_id: int):

    for index, product in enumerate(products):
        if product["id"] == product_id:
            deleted_product=products.pop(index)

            return {"message": "Product Deleted Successfully",
                    "product": deleted_product}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product Not Found"
    )