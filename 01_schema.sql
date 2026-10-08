CREATE TABLE suppliers (supplier_id INTEGER PRIMARY KEY, supplier_name TEXT, category TEXT, country TEXT);
CREATE TABLE purchase_orders (
  po_id INTEGER PRIMARY KEY, supplier_id INTEGER REFERENCES suppliers(supplier_id),
  order_date DATE, promised_date DATE, delivery_date DATE,
  qty_ordered INTEGER, qty_received INTEGER, qty_defective INTEGER,
  unit_price REAL, market_price REAL);
