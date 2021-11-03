/* Maksim Kovtun 2021-10-28 Initial

 */
DROP VIEW  IF EXISTS  custs;

DROP TABLE IF EXISTS order_contents, orders CASCADE;
DROP TABLE IF EXISTS cat_order_state CASCADE;

DROP TABLE IF EXISTS basket_items CASCADE;
DROP TABLE IF EXISTS baskets CASCADE;

DROP TABLE IF EXISTS customers CASCADE;



DROP TABLE IF EXISTS item_special_properties CASCADE;
DROP TABLE IF EXISTS items CASCADE;

DROP TABLE IF EXISTS product_main_properties CASCADE;
DROP TABLE IF EXISTS products CASCADE;


DROP TABLE IF EXISTS cat_main_properties, cat_special_properties CASCADE;
DROP TABLE IF EXISTS category CASCADE;


-- CATEGORY SECTION

CREATE TABLE category(
	id 					serial 			PRIMARY KEY ,
	parent_id 			INTEGER,
	category_name 		varchar(255) 	NOT NULL default '' ,
	short_description 	varchar(255),
	description 		varchar(255),
	image 				varchar(255)
);
comment on table category is 'category of the items';	
comment on column category.id is 'id';
comment on column category.parent_id  is 'link to the parent category, if applicable';
comment on column category.category_name  is 'name of the category';
comment on column category.short_description  is 'short description, up to 10 words';
comment on column category.description  is 'description of the category';
comment on column category.image  is 'link to the image (path to the hosting''s file or URI)';

-- approximately 4+4+21+101+256+101 = 487 bytes/category = 100 categories (50K)
grant select on category to netomerch_dbuser;




-- CUSTOMER SECTION
CREATE TABLE customers(
	id 				SERIAL 			PRIMARY KEY,
	first_name 		varchar(100),
	last_name 		varchar(100),
	password 		varchar(100),
	phone 			varchar(100),
	email 			varchar(100),
	address 		varchar(100),
	ip				varchar(100),
	is_registered 	boolean 		default False,
	is_active 		boolean 		default True
);
comment on table customers is 'information about registered customers';
comment on column customers.id is 'id';
-- approximately 4+31+31+21+31+11+21+16+1+1 = 168 bytes/user = 10.000 users (1600K)
grant select, insert, update, delete on customers to netomerch_dbuser;


CREATE TABLE cat_special_properties(
	id 				SERIAL 			PRIMARY KEY,
	property_name 	varchar(255),
	description 	varchar(255)
);
comment on table cat_special_properties is 'catalogue of the special (for items) properties';
comment on column cat_special_properties.id is 'id';
comment on column cat_special_properties.property_name is 'name of the special property';
comment on column cat_special_properties.id is 'description of the special property (for example, for hint in the admin board)';
-- approximately 4+21+201 = 487 bytes/category = 1000 main properties (220K)

grant select on cat_special_properties to netomerch_dbuser;











-- ITEM SECTION
CREATE TABLE items(
	id 					SERIAL 			PRIMARY KEY,
	category_id 		INTEGER,
	default_price 		money,
	item_name 			varchar(255) 	NOT NULL,
	short_description 	varchar(255),
	description 		varchar(255)
	, CONSTRAINT fk_items_category	FOREIGN KEY (category_id) REFERENCES 	category(id)
);
comment on table items is 'items separated by special properties';
comment on column items.id is 'id';
comment on column items.category_id is 'reference to the product';
comment on column items.default_price is 'default price';
comment on column items.item_name is 'name of the item';
comment on column items.short_description is 'short description, up to 10 words';
comment on column items.description is 'description of the item';

-- approximately 4+4+31+101+256 = 396 bytes/item * 100.000 items (39000K)
grant select on items to netomerch_dbuser;


CREATE TABLE item_special_properties(
	id 					SERIAL 	PRIMARY KEY,
	special_property_id INTEGER,
	item_id 			INTEGER,
	d_value 			timestamp,
	s_value 			varchar(255),
	n_value 			real,
	text_value 			varchar(255)
	, CONSTRAINT fk_item_sp_items		FOREIGN KEY (item_id) 				REFERENCES items(id)
	, CONSTRAINT fk_item_sp_cat_sp		FOREIGN KEY (special_property_id) 	REFERENCES cat_special_properties(id)
);
comment on table item_special_properties is 'table contains values of special properties for item';	
comment on column item_special_properties.id is 'id';
comment on column item_special_properties.special_property_id is 'reference to refbook of special properties';
comment on column item_special_properties.item_id is 'reference to items';
comment on column item_special_properties.d_value is 'value for d type property';
comment on column item_special_properties.s_value is 'value for s type property';
comment on column item_special_properties.n_value is 'value for n type property';
comment on column item_special_properties.text_value is 'text equivalent for property';
-- approximately 4+4+8+21+4+21 = 62 bytes/special property = 10 properties/item * 100.000 items (60000K)
grant select on item_special_properties to netomerch_dbuser;



-- ORDER SECTION

CREATE TABLE cat_order_state(
	id 			SERIAL 			PRIMARY KEY,
	state_name 	varchar(100) 	not null,
	description varchar(255) 
);
comment on table cat_order_state is 'reference book of order states';
comment on column cat_order_state.id is 'id';
comment on column cat_order_state.state_name is 'name of an order''s state, for example - paying';
comment on column cat_order_state.description is 'description of an order''s state';

-- approximately 4+11+201 = 216 bytes/state = 10 states (2K)
grant select on cat_order_state to netomerch_dbuser;


CREATE TABLE orders (
	id 					serial 			PRIMARY KEY,
	uid 				varchar(100), 
	order_created_at 	timestamp 		NOT NULL,
	order_finished_at 	timestamp 		NOT NULL,
	order_state_id 		INTEGER, 
	order_updated_at 	timestamp 		NOT NULL,
	discount_program 	INTEGER,
	customer_id 		INTEGER,
	cust_address 		varchar(255),
	cust_phone 			varchar(100),
	cust_email 			varchar(100),
	order_delivery_at 	timestamp,
	total_sum 			money
	, CONSTRAINT fk_orders_cat_os		FOREIGN KEY (order_state_id)  	REFERENCES 	cat_order_state(id)
	, CONSTRAINT fk_orders_customers	FOREIGN KEY (customer_id)  		REFERENCES  customers(id) 
);
comment on table orders is 'order''s information';	
comment on column orders.id is 'id';
comment on column orders.uid is 'unique identifier of order';
comment on column orders.order_created_at is 'timestamp of creation an order';
comment on column orders.order_finished_at is 'timestamp of finishing an order';
comment on column orders.order_state_id is 'reference to order_state';
comment on column orders.order_updated_at is 'timestamp of the last update of the order';
comment on column orders.discount_program is 'field for future feature :)';
comment on column orders.customer_id is 'reference to customers';
comment on column orders.cust_address is 'delivery address if applicable';
comment on column orders.cust_phone is 'cusomer''s phone if applicable';
comment on column orders.cust_email is 'customer''s e-mail if applicable';
comment on column orders.order_delivery_at is 'delivery date and time if applicable';
comment on column orders.total_sum is 'total sum of the order';
-- approximately 8+8+4+4+201+11+21+8 = 265 bytes/order = 100.000 orders (25800K)
grant select, insert, update, delete on orders to netomerch_dbuser;

create table order_contents(
	id 			serial 		PRIMARY KEY,
	order_id	integer 	NOT NULL,
	item_id		integer		NOT null
	, constraint fk_order_conts_orders foreign key (order_id) references orders(id)
	, constraint fk_order_conts_items foreign key (item_id) references items(id)	
);
comment on table order_contents is 'order contents';
comment on column order_contents.id is 'id';
comment on column order_contents.order_id is 'referece to orders';
comment on column order_contents.item_id is 'reference to items';

-- approximately 4+4+4 = 12 bytes/item in order = 100.000 orders * 10 items in order (11700K)
grant select, insert, update, delete on orders to netomerch_dbuser;
	



