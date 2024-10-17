from eralchemy import render_er

# ER Model for the plant store
models = """
[auth_user]
*id
username

[supplier]
*id
company_name
contact_number
address
user_id

[category]
*id
name
description

[plant]
*id
name
description
price
image
stock
supplier_id
category_id

[customer]
*id
first_name
last_name
email
address
user_id

[cart]
*id
user_id

[cart_item]
*id
quantity
cart_id
plant_id

[order]
*id
order_date
quantity
customer_id
plant_id

auth_user |o--|{ supplier:user_id
auth_user |o--|{ customer:user_id
supplier |o--o{ plant:supplier_id
category |o--o{ plant:category_id
customer |o--o{ order:customer_id
plant |o--o{ order:plant_id
cart |o--o{ cart_item:cart_id
plant |o--o{ cart_item:plant_id
"""

# Generate and save the ER diagram
render_er(models, 'plant_store_er_diagram.png')
