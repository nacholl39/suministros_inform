# Primero importamos las librerías necesarias.
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots


""" A continuación, creamos una instancia de la aplicación Flask, se establece una clave
secreta y se configura la URI de la base de datos. Además, se crea una instancia de 
SQLAlchemy para interactuar con la base de datos. """
app = Flask(__name__)
app.secret_key = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


""" A continuación, se definen los modelos de la base de datos. Cada modelo es una clase y
 sus atributos representan las columnas de la tabla en la base de datos."""

class Product(db.Model):
    """ Clase Product.
    Hace referencia a la tabla de productos en la cual guardamos los datos de cada producto.
    Contiene los atributos: id, name, description, precio_costo, precio_venta, stock, 
    quantity y supplier_id.
    args:
      -id: Es el identificador del producto, es de tipo int y es la clave primaria.
      -name: Es el nombre del producto, es de tipo str y no puede ser nulo.
      -description: Es la descripción del producto, es de tipo str y no puede ser nulo.
      -precio_costo: Es el precio de costo del producto, es de tipo float y no puede ser
       nulo.
      -precio_venta: Es el precio de venta del producto, es de tipo float y no puede ser 
       nulo.
      -stock, quantity: Es la cantidad de productos en stock, es de tipo int y no puede ser 
       nulo.
      -supplier_id: Es el identificador del proveedor, es de tipo int y no puede ser nulo. """


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    precio_costo = db.Column(db.Float, nullable=False)
    precio_venta = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)  
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)

    """ El método __repr__ nos aporta una representación legible en cadena del objeto. """
    def __repr__(self):
        return f'<Product {self.name}>'


class Supplier(db.Model):
    """ Clase Supplier.
    Hace referencia a la tabla de proveedores en la cual guardamos los datos de cada proveedor.
    Contiene los atributos: id, company_name, phone, address, cif y products.
    args:
      -id: Es el identificador del producto, es de tipo int y es la clave primaria.
      -company_name: Es el nombre de la empresa, es de tipo str y no puede ser nulo.
      -phone: Es el número de teléfono de la empresa, es de tipo str y no puede ser nulo.
      -address: Es la dirección de la empresa, es de tipo str y no puede ser nulo.
      -cif: Es el CIF de la empresa, es de tipo str y no puede ser nulo.
      -products: Es la relación con la tabla Product, es de tipo str y no puede ser nulo."""


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    cif = db.Column(db.String(20), nullable=False)
    products = db.relationship('Product', backref='supplier', lazy=True)

    """ El método __repr__ nos aporta una representación legible en cadena del objeto. """
    def __repr__(self):
        return f'<Supplier {self.company_name}>'

class User(db.Model):
    """ Clase User.
    Hace referencia a la tabla de usuarios en la cual guardamos los datos de cada usuario.
    Contiene los atributos: id, username, password, email e is_admin.
    args:
      -id: Es el identificador del producto, es de tipo int y es la clave primaria.
      -username: Es el nombre de usuario, es de tipo str y no puede ser nulo.
      -password: Es la contraseña del usuario, es de tipo str y no puede ser nulo.
      -email: Es el correo electrónico del usuario, es de tipo str y no puede ser nulo.
      -is_admin: Es un booleano que indica si el usuario es administrador o no, es de tipo
       bool y no puede ser nulo."""


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    """ El método __repr__ nos aporta una representación legible en cadena del objeto. """
    def __repr__(self):
        return f'<User {self.username}>'
    

class Sale(db.Model):
    """ Clase Sale.
    Hace referencia a la tabla de ventas en la cual guardamos los datos de cada venta.
    Contiene los atributos: id, sale_date, product_name, supplier_name, quantity, selling_price,
    args:
      -id: Es el identificador del producto, es de tipo int y es la clave primaria.
      -sale_date: Es la fecha de la venta, es de tipo date y no puede ser nulo.
      -product_name: Es el nombre del producto, es de tipo str y no puede ser nulo.
      -supplier_name: Es el nombre del proveedor, es de tipo str y no puede ser nulo.
      -quantity: Es la cantidad de productos vendidos, es de tipo int y no puede ser nulo.
      -selling_price: Es el precio de venta del producto, es de tipo float y no puede ser nulo.
      -total_price: Es el precio total de la venta, es de tipo float y no puede ser nulo.
      -cost_price: Es el precio de costo del producto, es de tipo float y no puede ser nulo.
      -total_profit: Es el beneficio total de la venta, es de tipo float y no puede ser nulo."""


    id = db.Column(db.Integer, primary_key=True)
    sale_date = db.Column(db.Date, nullable=False)
    product_name = db.Column(db.String(50), nullable=False)
    supplier_name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    selling_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    cost_price = db.Column(db.Float, nullable=False)
    total_profit = db.Column(db.Float, nullable=False)

    """ El método __repr__ nos aporta una representación legible en cadena del objeto. """
    def __repr__(self):
        return f'<Sale {self.id}>'



"""  Aquí se crea la base de datos y las tablas correspondientes utilizando el
 contexto de la aplicación Flask. """
with app.app_context():
    db.create_all()

""" Ruta principal. Esta es la ruta principal de la aplicación. Cuando un usuario accede
a la ruta raíz ("/"), se renderiza la plantilla HTML llamada "index.html". """
@app.route('/')
def index():
    return render_template('index.html')


""" Ruta de login. Esta ruta maneja la funcionalidad de inicio de sesión. Si se realiza
una solicitud POST con un nombre de usuario y contraseña válidos, el usuario 
iniciará sesión y se establecerá la sesión del usuario. En caso contrario, se 
mostrará un mensaje de error. """
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Implementación de la ruta de inicio de sesión
    # Permite a los usuarios iniciar sesión utilizando un formulario de inicio de sesión
    # Verifica las credenciales y establece la sesión del usuario si son válidas
    # Utiliza la función flash para mostrar mensajes de éxito o error
    # Redirige a la página de inicio de sesión si el usuario no ha iniciado sesión
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['user_id'] = user.id
            flash('Login successful', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')



"""  Ruta de logout. Esta ruta maneja la funcionalidad de cierre de sesión. Cuando un 
 usuario accede a esta ruta, se borra la sesión del usuario y se redirige a la página
 de inicio de sesión. """
@app.route('/logout')
def logout():
    # Implementación de la ruta de cierre de sesión
    # Elimina la sesión del usuario y redirige a la página de inicio de sesión
    # Utiliza la función flash para mostrar mensajes de éxito o error

    session.pop('user_id', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))


""" Ruta de panel de control. Esta ruta maneja la funcionalidad del panel de control.
Si el usuario ha iniciado sesión, se renderiza la plantilla HTML correspondiente."""
@app.route('/dashboard')
def dashboard():
    # Implementación de la ruta del panel de control
    # Verifica si el usuario ha iniciado sesión antes de mostrar el panel de control
    # Redirige al usuario a la página de inicio de sesión si no ha iniciado sesión
    # Obtiene el ID de usuario de la sesión y recupera el objeto de usuario correspondiente de la base de datos
    # Consulta productos con un stock bajo y los filtra por aquellos que tienen un stock menor o igual al 90% de su cantidad
    # Si el usuario es un administrador, obtiene todos los productos y proveedores de la base de datos
    # Renderiza la plantilla HTML "admin_dashboard.html" con los productos, proveedores y productos de bajo stock
    # Si el usuario no es un administrador, renderiza la plantilla HTML "client_dashboard.html" con los productos de bajo stock



    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get(user_id)

    low_stock_products = Product.query.filter(Product.stock <= 0.9 * Product.quantity)

    if user.is_admin:
        products = Product.query.all()
        suppliers = Supplier.query.all()
        return render_template('admin_dashboard.html', products=products, suppliers=suppliers, low_stock_products=low_stock_products)
    else:
        return render_template('client_dashboard.html', low_stock_products=low_stock_products)



# Ruta de agregar un producto
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    # Implementación de la ruta para agregar un producto
    # Verifica si el usuario ha iniciado sesión antes de permitir agregar un producto
    # Redirige al usuario a la página de inicio de sesión si no ha iniciado sesión


    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Procesa el formulario cuando se envía por el método POST
        # Crea un nuevo objeto de Producto
        # Obtiene los datos del formulario (nombre, descripción, precio de costo, precio de venta, stock, cantidad y ID del proveedor)
        # Crea un nuevo objeto de Producto con los datos proporcionados
        # Agrega el nuevo producto a la sesión de la base de datos
        # Realiza la confirmación de la sesión para guardar los cambios en la base de datos
        # Muestra un mensaje flash indicando que el producto se agregó correctamente
        # Redirige al usuario al panel de control

        product = Product()
        name = request.form['name']
        description = request.form['description']
        precio_costo = float(request.form['precio_costo'])
        precio_venta = float(request.form['precio_venta'])
        stock = int(request.form['stock'])
        quantity = int(request.form['quantity'])
        supplier_id = int(request.form['supplier'])

        product = Product(name=name, description=description, precio_costo=precio_costo, precio_venta=precio_venta, stock=stock, quantity=quantity, supplier_id=supplier_id)
        
        db.session.add(product)
        db.session.commit()

        flash('Product added successfully', 'success')
        return redirect(url_for('dashboard'))

    # Obtiene todos los proveedores de la base de datos
    # Renderiza la plantilla HTML "add_product.html" con la lista de proveedores
    suppliers = Supplier.query.all()
    return render_template('add_product.html', suppliers=suppliers)



# Ruta de agregar un proveedor. Esta ruta maneja la funcionalidad de agregar un proveedor.
@app.route('/add_supplier', methods=['GET', 'POST'])
def add_supplier():
    # Implementación de la ruta para agregar un proveedor
    # Verifica si el usuario ha iniciado sesión antes de permitir agregar un proveedor
    # Redirige al usuario a la página de inicio de sesión si no ha iniciado sesión

    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Procesa el formulario cuando se envía por el método POST
        # Obtiene los datos del formulario (nombre de la empresa, teléfono, dirección y CIF)
        # Crea un nuevo objeto de Proveedor con los datos proporcionados
        # Agrega el nuevo proveedor a la sesión de la base de datos
        # Realiza la confirmación de la sesión para guardar los cambios en la base de datos
        # Muestra un mensaje flash indicando que el proveedor se agregó correctamente
        # Redirige al usuario al panel de control

        company_name = request.form['company_name']
        phone = request.form['phone']
        address = request.form['address']
        cif = request.form['cif']

        supplier = Supplier(company_name=company_name, phone=phone, address=address, cif=cif)
        db.session.add(supplier)
        db.session.commit()

        flash('Supplier added successfully', 'success')
        return redirect(url_for('dashboard'))
    
    # Renderiza la plantilla HTML "add_supplier.html"
    return render_template('add_supplier.html')


# Ruta para agregar una venta. Esta ruta maneja la funcionalidad de agregar una venta.
@app.route('/add_sale', methods=['POST'])
def add_sale():
    # Implementación de la ruta para agregar una venta
    # Verifica si el usuario ha iniciado sesión antes de permitir agregar una venta
    # Redirige al usuario a la página de inicio de sesión si no ha iniciado sesión


    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Procesa el formulario cuando se envía por el método POST
        # Obtiene los datos del formulario (ID del producto y cantidad)
        # Obtiene el objeto del producto correspondiente al ID proporcionado
        # Verifica si el producto existe en la base de datos
        # Si el producto no existe, muestra un mensaje flash de error y redirige al panel de control
        # Verifica si la cantidad solicitada excede el stock disponible del producto
        # Si la cantidad es mayor que el stock, muestra un mensaje flash de error y redirige al panel de control
        # Crea un nuevo objeto de Venta con los datos proporcionados (fecha de venta, nombre del producto, nombre del proveedor, cantidad, precio de venta, precio total, precio de costo, ganancia total)
        # Actualiza el stock del producto restando la cantidad vendida
        # Agrega la nueva venta a la sesión de la base de datos
        # Realiza la confirmación de la sesión para guardar los cambios en la base de datos
        # Muestra un mensaje flash indicando que la venta se agregó correctamente
        # Redirige al usuario al panel de control

        product_id = int(request.form['product'])
        quantity = int(request.form['quantity'])

        product = Product.query.get(product_id)

        if product is None:
            flash('Invalid product', 'error')
            return redirect(url_for('dashboard'))

        if quantity > product.stock:
            flash('Insufficient stock', 'error')
            return redirect(url_for('dashboard'))

        sale = Sale(
            sale_date=datetime.now().date(),
            product_name=product.name,
            supplier_name=product.supplier.company_name,
            quantity=quantity,
            selling_price=product.precio_venta,
            total_price=product.precio_venta * quantity,
            cost_price=product.precio_costo * quantity,
            total_profit=(product.precio_venta - product.precio_costo) * quantity
        )

        product.stock -= quantity
        db.session.add(sale)
        db.session.commit()

        flash('Sale added successfully', 'success')
        return redirect(url_for('dashboard'))

    # Redirige al usuario al panel de control
    return redirect(url_for('dashboard'))


# Ruta 
@app.route('/charts')
def charts():
    # Implementación de la ruta para mostrar gráficos
    # Verifica si el usuario ha iniciado sesión antes de mostrar los gráficos
    # Redirige al usuario a la página de inicio de sesión si no ha iniciado sesión



    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Obtiene todos los proveedores de la base de datos
    suppliers = Supplier.query.all()

    # Inicializa listas para almacenar datos de ventas y ganancias por proveedor
    sales_data = []
    profits_data = []

    # Itera sobre los proveedores y obtiene las ventas y ganancias totales para cada proveedor
    for supplier in suppliers:
        # Obtiene todas las ventas asociadas al proveedor actual
        supplier_sales = Sale.query.filter_by(supplier_name=supplier.company_name).all()
        
        # Calcula el total de ventas sumando la cantidad vendida en cada venta
        total_sales = sum([sale.quantity for sale in supplier_sales])
        
        # Calcula las ganancias totales sumando las ganancias en cada venta
        total_profits = sum([sale.total_profit for sale in supplier_sales])
        
        # Agrega los datos de ventas y ganancias a las listas correspondientes
        sales_data.append(total_sales)
        profits_data.append(total_profits)

    # Crea una figura con dos gráficos de barras
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Sales by Supplier", "Profits by Supplier"))

    # Agrega el gráfico de barras de ventas al primer subplot
    fig.add_trace(go.Bar(x=[supplier.company_name for supplier in suppliers], y=sales_data, name='Sales'), row=1, col=1)
    
    # Agrega el gráfico de barras de ganancias al segundo subplot
    fig.add_trace(go.Bar(x=[supplier.company_name for supplier in suppliers], y=profits_data, name='Profits'), row=1, col=2)

    # Configura el diseño del gráfico para ocultar la leyenda
    fig.update_layout(showlegend=False)

    # Convierte la figura en HTML para poder mostrarla en la plantilla
    sales_chart_div = fig.to_html(full_html=False)
    profits_chart_div = fig.to_html(full_html=False)

    # Renderiza la plantilla 'admin_dashboard.html' con los datos de los gráficos y los proveedores
    return render_template('admin_dashboard.html', sales_chart_div=sales_chart_div, profits_chart_div=profits_chart_div, suppliers=suppliers)

""" Ruta gráfico de ventas. Esta ruta maneja la funcionalidad del gráfico de ventas. 
 Obtiene los datos necesarios de la base de datos para generar el gráfico de ventas 
 utilizando la biblioteca Plotly. Luego, renderiza la plantilla HTML "sales_chart.html"
 con los datos necesarios para el gráfico. """
@app.route('/sales_chart')
def sales_chart():
    # Implementación de la ruta del gráfico de ventas
    # Obtiene datos de la base de datos para generar el gráfico de ventas utilizando Plotly
    # Renderiza la plantilla HTML "sales_chart.html" con los datos necesarios para el gráfico


    if 'user_id' not in session:
        return redirect(url_for('login'))

    suppliers = Supplier.query.all()

    sales_data = []
    for supplier in suppliers:
        supplier_sales = Sale.query.filter_by(supplier_name=supplier.company_name).all()
        total_sales = sum([sale.quantity for sale in supplier_sales])
        sales_data.append(total_sales)

    fig = go.Figure(data=go.Bar(x=[supplier.company_name for supplier in suppliers], y=sales_data))
    sales_chart_div = fig.to_html(full_html=False)

    return render_template('sales_chart.html', sales_chart_div=sales_chart_div)


""" Ruta gráfico de beneficios. Esta ruta maneja la funcionalidad del gráfico de 
 beneficios. Obtiene los datos necesarios de la base de datos para generar el gráfico
  de beneficios utilizando la biblioteca Plotly. Luego, renderiza la plantilla HTML 
 "profits_chart.html" con los datos necesarios para el gráfico. """
@app.route('/profits_chart')
def profits_chart():
    # Implementación de la ruta del gráfico de beneficios
    # Obtiene datos de la base de datos para generar el gráfico de beneficios utilizando Plotly
    # Renderiza la plantilla HTML "profits_chart.html" con los datos necesarios para el gráfico

    if 'user_id' not in session:
        return redirect(url_for('login'))

    suppliers = Supplier.query.all()

    profits_data = []
    for supplier in suppliers:
        supplier_sales = Sale.query.filter_by(supplier_name=supplier.company_name).all()
        total_profits = sum([sale.total_profit for sale in supplier_sales])
        profits_data.append(total_profits)

    fig = go.Figure(data=go.Bar(x=[supplier.company_name for supplier in suppliers], y=profits_data))
    profits_chart_div = fig.to_html(full_html=False)

    return render_template('profits_chart.html', profits_chart_div=profits_chart_div)



""" Esta línea verifica si el archivo se está ejecutando directamente y, en ese caso, 
 inicia la aplicación Flask en modo de depuración. """
if __name__ == '__main__':
    app.run(debug=True)
