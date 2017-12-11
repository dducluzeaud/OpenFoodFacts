delete from subcategories;
delete from product;
delete from categories;
delete from replaced_product;

CREATE TABLE Categories (
    id_category SMALLINT(5) UNSIGNED PRIMARY KEY AUTO_INCREMENT ,
    category_name VARCHAR(255) NOT NULL
)engine=InnoDB
DEFAULT CHARACTER SET = utf8;

DROP TABLE IF EXISTS replacement_product;

CREATE TABLE Replacement_products(
    id_product_replacement SMALLINT(5) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    product_name_replacement VARCHAR(255)
)engine=InnoDB
DEFAULT CHARACTER SET = utf8;


DROP TABLE IF EXISTS Product;

CREATE TABLE Products (
    id_product SMALLINT(5) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255),
    quantity VARCHAR(255), 
    url_text VARCHAR(255),
    packaging VARCHAR(255),
    brand VARCHAR(255),
    origin VARCHAR(255),
    allegerns VARCHAR(255),
    traces VARCHAR(255),
    additives_number VARCHAR(5),
    additives TEXT,
    nutrition_score CHAR(1),
    product_name_replacement_id SMALLINT(5) UNSIGNED,
    subcategory_id SMALLINT(5) UNSIGNED,
    KEY fk_replacement_product_id (product_name_replacement_id),
    CONSTRAINT fk_replacement_product_id FOREIGN KEY (product_name_replacement_id) REFERENCES replacement_products(id_product_replacement)
)engine=InnoDb
DEFAULT CHARACTER SET = utf8;

DROP TABLE IF EXISTS Subcategory;

CREATE TABLE Subcategories(
    id_subcategory SMALLINT(5) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    subcategory_name VARCHAR(255),
    category_id SMALLINT(5) UNSIGNED,
    product_id SMALLINT(5) UNSIGNED,
    KEY fk_subcategory_id(category_id),
    KEY fk_product_id(product_id),
    CONSTRAINT fk_subcategory_id FOREIGN KEY(category_id) REFERENCES Categories(id_category),
    CONSTRAINT fk_product_id FOREIGN KEY(product_id) REFERENCES Products(id_product)
)engine=InnoDB
DEFAULT CHARACTER SET = utf8;







