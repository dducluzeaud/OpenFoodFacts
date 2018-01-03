DROP TABLE subcategories;
DROP TABLE product;
DROP TABLE categories;
DROP TABLE replaced_products;

CREATE TABLE Categories (
    category_name VARCHAR(255) NOT NULL PRIMARY KEY
)engine=InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE Replacement_products (
  id_product_replacement SMALLINT(5) AUTO_INCREMENT PRIMARY KEY,
  product_id smallint(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE Products (
    id_product SMALLINT(5) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255),
    quantity VARCHAR(255),
    url_text VARCHAR(255),
    packaging VARCHAR(255),
    brand VARCHAR(255),
    origin VARCHAR(255),
    allergens VARCHAR(255),
    traces VARCHAR(255),
    additives_number VARCHAR(5),
    additives TEXT,
    nutrition_score CHAR(1),
    product_replacement_id SMALLINT(5),
    added_date datetime,
    subcategory_id SMALLINT(5) UNSIGNED,
    KEY fk_replacement_product_id (product_replacement_id),
    CONSTRAINT fk_replacement_product_id FOREIGN KEY (product_replacement_id) REFERENCES replacement_products(id_product_replacement)
)engine=InnoDb
DEFAULT CHARACTER SET = utf8;

CREATE TABLE Subcategories(
    id_subcategory SMALLINT(5) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    subcategory_name VARCHAR(255),
    name_category VARCHAR(255) NOT NULL,
    KEY fk_name_category(name_category),
    CONSTRAINT fk_name_category FOREIGN KEY(name_category) REFERENCES Categories(category_name)
)engine=InnoDB
DEFAULT CHARACTER SET = utf8;
