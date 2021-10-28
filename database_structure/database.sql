/* Maksim Kovtun 2021-10-28 Initial

 */
DROP VIEW  IF EXISTS  custs;

DROP TABLE IF EXISTS custs, customers, customers_notregistered CASCADE;
DROP TABLE IF EXISTS  orders CASCADE;
DROP TABLE IF EXISTS cat_order_state CASCADE;

DROP TABLE IF EXISTS basket_items CASCADE;
DROP TABLE IF EXISTS baskets CASCADE;

DROP TABLE IF EXISTS items CASCADE;
DROP TABLE IF EXISTS item_special_properties CASCADE;

DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS product_main_properties CASCADE;


DROP TABLE IF EXISTS cat_main_properties, cat_special_properties CASCADE;
DROP TABLE IF EXISTS category CASCADE;


-- CATEGORY SECTION

CREATE TABLE category(
	id INT UNSIGNED auto_increment PRIMARY KEY COMMENT 'id',
	parent_id INT UNSIGNED comment 'link to the parent category, if applicable',
	name varchar(255) NOT NULL default '' comment 'name of the category',
	short_description varchar(255) comment 'short description, up to 10 words',
	description varchar(255) comment 'description of the category',
	image varchar(255) comment 'link to the image (path to the hosting''s file or URI)'
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8
COMMENT='category of the items';	
-- approximately 4+4+21+101+256+101 = 487 bytes/category = 100 categories (50K)




-- CUSTOMER SECTION
CREATE TABLE customers(
	id INT UNSIGNED auto_increment PRIMARY KEY COMMENT 'id increment +1 from 1',
	first_name varchar(100),
	last_name varchar(100),
	login varchar(100),
	password varchar(100),
	phone varchar(100),
	email varchar(100),
	address varchar(100),
	ip	varchar(100),
	is_active bool default True
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8
COMMENT='information about registered customers';
-- approximately 4+31+31+21+31+11+21+16+1 = 167 bytes/user = 5000 users (800K)

CREATE TABLE customers_notregistered(
	id INT PRIMARY KEY COMMENT 'id increment to -1 from -1',
	first_name varchar(100),
	last_name varchar(100),
	login varchar(100),
	password varchar(100),
	phone varchar(100),
	email varchar(100),
	address varchar(100),
	ip	varchar(100),
	is_active bool default True
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8
COMMENT='information about non registered AKA 1-click-order customers';
-- approximately 4+31+31+21+31+11+21+16+1 = 167 bytes/user = 5000 users (800K)

-- production: 
CREATE OR REPLACE VIEW custs AS
select 	id,
	first_name ,
	last_name,
	login,
	password,
	phone,
	email,
	address,
	ip,
	is_active
from customers
union all
select 	id,
	first_name ,
	last_name,
	login,
	password,
	phone,
	email,
	address,
	ip,
	is_active
from customers_notregistered;


/* dev: 

CREATE table custs AS
select 	id,
	first_name ,
	last_name,
	login,
	password,
	phone,
	email,
	address,
	ip,
	is_active
from customers
union all
select 	id,
	first_name ,
	last_name,
	login,
	password,
	phone,
	email,
	address,
	ip,
	is_active
from customers_notregistered;

*/




-- PROPERTY SECTION

CREATE TABLE cat_main_properties(
	id INT UNSIGNED auto_increment PRIMARY KEY COMMENT 'id',
	property_type char(1) comment 'type of the property d(ate), s(tring), n(umeric)',
	name varchar(255) comment 'name of the main property',
	description varchar(255) comment 'description of the main property (for example, for hint in the admin board)'
) 
ENGINE=InnoDB
DEFAULT CHARSET=utf8
COMMENT='catalogue of the main properties';	
-- approximately 4+21+201 = 487 bytes/category = 1000 main properties (220K)

CREATE TABLE cat_special_properties(
	id INT UNSIGNED auto_increment PRIMARY KEY COMMENT 'id',
	name varchar(255) comment 'name of the special property',
	description varchar(255) comment 'description of the special property (for example, for hint in the admin board)'
) 
ENGINE=InnoDB
DEFAULT CHARSET=utf8
COMMENT='catalogue of the special (for items) properties';	
-- approximately 4+21+201 = 487 bytes/category = 1000 main properties (220K)







-- PRODUCT SECTION

CREATE TABLE products(
	id INT UNSIGNED auto_increment PRIMARY KEY COMMENT 'id',
	category_id INT UNSIGNED comment 'reference to category',
	name varchar(255) NOT NULL default '' comment 'name of the product',
	short_description varchar(255) comment 'short description, up to 10 words',
	description varchar(255) comment 'description of the product',
	image varchar(255) comment 'link to the image (path to the hosting''s file or URI)', /* we can CHANGE FOR multiply images*/
	FOREIGN KEY (category_id) REFERENCES category(id)
	)
ENGINE=InnoDB
DEFAULT CHARSET=utf8
COMMENT='products (items grouping by main properties)';	
-- approximately 4+4+31+51+256+201 = 547 bytes/product = 1000 products (550K)


CREATE TABLE product_main_properties(
	id BIGINT UNSIGNED auto_increment PRIMARY KEY COMMENT 'id',
	main_property_id INT UNSIGNED REFERENCES cat_main_properties(id),
	product_id INT UNSIGNED REFERENCES products(id),
	d_value DATETIME comment 'value for d type property',
	s_value varchar(255) comment 'value for s type property',
	n_value NUMERIC comment 'value for n type property',
	text varchar(255) comment 'text equivalent for property' /*we can make it AS calculated*/
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8
COMMENT='table contains values of main properties for product';	
-- approximately 4+4+8+21+4+21 = 62 bytes/main property = 10 properties/produc 1000 products (600K)






-- ITEM SECTION
CREATE TABLE items(
	id INT UNSIGNED auto_increment PRIMARY KEY COMMENT 'id',
	product_id INT UNSIGNED  comment 'reference to the product',
	default_price NUMERIC comment 'default price',
	name varchar(255) NOT NULL comment 'name of the item',
	short_description varchar(255) comment 'short description, up to 10 words',
	description varchar(255) comment 'description of the item',
	CONSTRAINT FOREIGN KEY (product_id) REFERENCES products(id)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8
COMMENT='items separated by special properties, e.g. 1 product has 2 sizes, therefore it has 2 items';	
-- approximately 4+4+31+101+256 = 396 bytes/item * 100.000 items (39000K)

CREATE TABLE item_special_properties(
	id BIGINT UNSIGNED auto_increment PRIMARY KEY COMMENT 'id',
	special_property_id INT UNSIGNED REFERENCES cat_special_properties(id),
	item_id INT UNSIGNED REFERENCES products(id),
	d_value DATETIME comment 'value for d type property',
	s_value varchar(255) comment 'value for s type property',
	n_value NUMERIC comment 'value for n type property',
	text varchar(255) comment 'text equivalent for property' /* we can make it AS calculated */
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8
COMMENT='table contains values of special properties for item';	
-- approximately 4+4+8+21+4+21 = 62 bytes/special property = 10 properties/item * 100.000 items (60000K)


-- BACKET SECTION

CREATE TABLE baskets (
	id BIGINT UNSIGNED auto_increment PRIMARY KEY COMMENT 'id',
	cust_id INT UNSIGNED comment 'reference to custs'
	/*,
	CONSTRAINT FOREIGN KEY (cust_id) REFERENCES custs(id)*/
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8
COMMENT='baskets info';
-- approximately 8+4+4+4 = 18 bytes/basketspecial property = 10 properties/item * 100.000 items (60000K)

CREATE TABLE basket_items (
	id BIGINT UNSIGNED auto_increment PRIMARY KEY COMMENT 'id',
	basket_id BIGINT UNSIGNED  comment 'reference to baskets',
	item_id INT UNSIGNED COMMENT 'reference to items',
	amount INT comment 'amount of item',
	discount_program INT comment 'field for future feature :)',
	total_sum_for_items NUMERIC comment 'total sum of item*amout - discount'
	, CONSTRAINT FOREIGN KEY (item_id)  REFERENCES items(id)
	, CONSTRAINT FOREIGN KEY (basket_id)  REFERENCES baskets(id)
	
	
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8
COMMENT='basket with items';	
-- approximately 8+8+4+4+4+4 = 32 bytes/item = 10 items in 1 baskets * 100.000 baskets (31200K)




-- ORDER SECTION

CREATE TABLE cat_order_state(
	id INT UNSIGNED auto_increment PRIMARY KEY COMMENT 'id',
	name varchar(100) not null comment 'name of an order''s state, for example - paying',
	description varchar(255) comment 'description of an order''s state'
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8
COMMENT='reference book of order states';
-- approximately 4+11+201 = 216 bytes/state = 10 states (2K)


CREATE TABLE orders (
	id BIGINT UNSIGNED auto_increment PRIMARY KEY COMMENT 'id',
	order_created_at datetime NOT NULL comment 'datetime of creation an order',
	order_finished_at datetime NOT NULL comment 'datetime of finishing an order',
	order_state_id int UNSIGNED comment 'reference to order_state', 
	order_updated_at datetime NOT NULL comment 'datetime of updating an order',
	basket_id BIGINT UNSIGNED comment 'reference to backet',
	discount_program int comment 'field for future feature :)',
	cust_id INT UNSIGNED COMMENT 'reference to custs ',
	cust_address varchar(255) COMMENT 'delivery address if applicable',
	cust_phone varchar(100) comment 'cusomer''s phone if applicable',
	cust_email varchar(100) comment 'customer''s e-mail if applicable',
	order_delivery_at datetime comment 'delivery date and time if applicable',
	total_sum NUMERIC comment 'total sum of an order'
	, CONSTRAINT FOREIGN KEY (order_state_id)  REFERENCES cat_order_state(id)
	, CONSTRAINT FOREIGN KEY (basket_id)  REFERENCES  baskets(id) 
	/*, CONSTRAINT FOREIGN KEY (cust_id)  REFERENCES  custs(id) */
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8
COMMENT='order''s information';	
-- approximately 8+8+4+4+201+11+21+8 = 265 bytes/order = 100.000 orders (25800K)




