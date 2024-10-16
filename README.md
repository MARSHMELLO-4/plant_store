<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Plant E-commerce Store built with Django. Customers can browse, order plants, while suppliers can manage listings and orders.">
</head>
<body>

<h1>Plant E-commerce Store (Django Web Application)</h1>

<p>
    This repository contains the code for a plant e-commerce store built using Django. The application allows customers to browse through various plants, add them to their cart, and place orders, while suppliers can manage their plant listings and view orders. The system supports customer and supplier functionalities with separate sign-up and dashboard views.
</p>

<h2>Features</h2>

<h3>Customer Features</h3>
<ul>
    <li><strong>Browse Plants:</strong> Customers can browse plants listed on the website, categorized for easier navigation.</li>
    <li><strong>Plant Details:</strong> Detailed information about each plant is available, including its description, price, stock, and image.</li>
    <li><strong>User Authentication:</strong> Customers can sign up, log in, and log out. They need to log in to add items to their cart or place an order.</li>
    <li><strong>Cart Management:</strong> Users can add plants to their cart, update quantities, or remove items.</li>
    <li><strong>Order Placement:</strong> Customers can place orders for plants in their cart and view their order history.</li>
    <li><strong>Profile Management:</strong> Customers can update their personal information and address.</li>
</ul>

<h3>Supplier Features</h3>
<ul>
    <li><strong>Supplier Authentication:</strong> Suppliers have a separate sign-up and login system.</li>
    <li><strong>Supplier Dashboard:</strong> Once logged in, suppliers can manage their plant listings and view customer orders.</li>
    <li><strong>Add/Edit/Delete Plants:</strong> Suppliers can add new plants to the store, update existing listings, or delete them if needed.</li>
    <li><strong>Order Management:</strong> Suppliers can view all the orders placed for their plants, organized by the customer.</li>
</ul>

<h3>General Features</h3>
<ul>
    <li><strong>Separate Customer and Supplier Dashboards:</strong> Customers and suppliers each have their own set of functionalities and dashboards.</li>
    <li><strong>Order Success Page:</strong> After placing an order, customers are redirected to a success page.</li>
    <li><strong>Complete Profile:</strong> Customers can complete their profile after registration, including updating their contact details and address.</li>
</ul>

<h2>Project Structure</h2>

<h3>Models</h3>
<ul>
    <li><strong>Customer:</strong> Stores customer details like name, email, and address.</li>
    <li><strong>Supplier:</strong> Represents suppliers who can list plants for sale.</li>
    <li><strong>Category:</strong> Defines the plant categories available in the store.</li>
    <li><strong>Plant:</strong> Represents the plants listed in the store, including details like name, description, price, image, and stock quantity.</li>
    <li><strong>Cart:</strong> Each user has a cart that holds the items they intend to buy.</li>
    <li><strong>CartItem:</strong> Tracks individual plant items in a customer's cart.</li>
    <li><strong>Order:</strong> Records the details of orders placed by customers, including the plant, quantity, and customer information.</li>
</ul>

<h3>Forms</h3>
<ul>
    <li><strong>CustomerSignUpForm:</strong> Used for customer registration.</li>
    <li><strong>SupplierSignUpForm:</strong> Used for supplier registration.</li>
    <li><strong>CustomerUpdateForm:</strong> Allows customers to update their profile information.</li>
    <li><strong>SupplierUpdateForm:</strong> Allows suppliers to update their profile information.</li>
    <li><strong>PlantForm:</strong> Form used by suppliers to add or edit plant details.</li>
</ul>

<h3>Views</h3>
<ul>
    <li><strong>Customer Views:</strong> Plant browsing, cart management, profile updates, and order placement.</li>
    <li><strong>Supplier Views:</strong> Plant management, supplier dashboard, and order views.</li>
    <li><strong>Authentication Views:</strong> Handle user login, logout, and signup for both customers and suppliers.</li>
</ul>

<h2>Installation and Setup</h2>
<ol>
    <li><strong>Clone the repository:</strong>
        <pre><code>git clone https://github.com/MARSHMELLO-4/plant_store</code></pre>
    </li>
    <li><strong>Install dependencies:</strong> Use a virtual environment and install Django:
        <pre><code>pip install -r requirements.txt</code></pre>
    </li>
    <li><strong>Run migrations:</strong>
        <pre><code>python manage.py migrate</code></pre>
    </li>
    <li><strong>Create a superuser:</strong>
        <pre><code>python manage.py createsuperuser</code></pre>
    </li>
    <li><strong>Start the development server:</strong>
        <pre><code>python manage.py runserver</code></pre>
    </li>
    <li><strong>Access the app:</strong> Open your web browser and go to <code>http://127.0.0.1:8000/</code> to access the store.</li>
</ol>

<h2>Usage</h2>

<h3>Customer Side</h3>
<ul>
    <li><strong>Signup or Login:</strong> Create a customer account or log in to an existing account.</li>
    <li><strong>Browse Plants:</strong> Explore the available plants and view details.</li>
    <li><strong>Add to Cart:</strong> Add desired plants to your cart.</li>
    <li><strong>Place an Order:</strong> Proceed to checkout by placing an order for the items in the cart.</li>
    <li><strong>View Orders:</strong> After placing an order, customers can view their past orders.</li>
</ul>

<h3>Supplier Side</h3>
<ul>
    <li><strong>Supplier Signup/Login:</strong> Suppliers sign up separately from customers and manage plants from their dashboard.</li>
    <li><strong>Manage Plants:</strong> Suppliers can add, edit, and delete plants from the store.</li>
    <li><strong>View Orders:</strong> Suppliers can see customer orders for their listed plants.</li>
</ul>

<h2>File Structure Overview</h2>
<ul>
    <li><code>models.py</code>: Defines the database models such as <code>Customer</code>, <code>Supplier</code>, <code>Plant</code>, <code>Order</code>, etc.</li>
    <li><code>views.py</code>: Contains the view logic for both customers and suppliers.</li>
    <li><code>forms.py</code>: Defines forms for customer and supplier registration and updating plant information.</li>
    <li><code>urls.py</code>: Defines URL routes for the application.</li>
    <li><code>templates/</code>: Holds the HTML templates for rendering the front-end.</li>
    <li><code>static/</code>: Contains static assets like CSS and images.</li>
</ul>

<h2>Contributing</h2>
<p>Contributions are welcome! If you encounter any issues or have suggestions, feel free to open an issue or submit a pull request.</p>
<ol>
    <li>Fork the repository.</li>
    <li>Create your feature branch (<code>git checkout -b feature/YourFeature</code>).</li>
    <li>Commit your changes (<code>git commit -m 'Add some feature'</code>).</li>
    <li>Push to the branch (<code>git push origin feature/YourFeature</code>).</li>
    <li>Open a pull request.</li>
</ol>

<h2>License</h2>
<p>This project is licensed under the MIT License. See the <code>LICENSE</code> file for more details.</p>

<h2>Acknowledgements</h2>
<p>This project was built using <a href="https://www.djangoproject.com/" target="_blank">Django</a> and various open-source libraries.</p>

</body>
</html>
