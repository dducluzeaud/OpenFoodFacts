DROP TABLE IF EXISTS categories;

CREATE TABLE Categories (
    id_category SMALLINT(5) UNSIGNED PRIMARY KEY AUTO_INCREMENT ,
    category_name VARCHAR(20) NOT NULL
)engine=InnoDB
DEFAULT CHARACTER SET = utf8;

DROP TABLE IF EXISTS Replaced_product;

CREATE TABLE Replaced_product(
    id_product_replaced SMALLINT(5) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    product_name_replaced VARCHAR(20)
)engine=InnoDB
DEFAULT CHARACTER SET = utf8;

DROP TABLE IF EXISTS Product;

CREATE TABLE Product (
    id_product SMALLINT(5) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255),
    quantity VARCHAR(255),
    url_text VARCHAR(255),
    packaging VARCHAR(255),
    brand VARCHAR(255),
    origin VARCHAR(255),
    allegerns VARCHAR(255),
    traces VARCHAR(255),
    additives_number TINYINT UNSIGNED,
    additives VARCHAR(255),
    nutrition_score CHAR(1),
    category_id SMALLINT(5) UNSIGNED,
    product_name_replaced_id SMALLINT(5) UNSIGNED,
    subcategory_id SMALLINT(5) UNSIGNED,
    KEY fk_category_id (category_id),
    KEY fk_replaced_product_id (product_name_replaced_id),
    CONSTRAINT fk_category_id FOREIGN KEY (category_id) REFERENCES Categories (id_category),
    CONSTRAINT fk_replaced_product_id FOREIGN KEY (product_name_replaced_id) REFERENCES Replaced_product(id_product_replaced)
)engine=InnoDb
DEFAULT CHARACTER SET = utf8;

DROP TABLE IF EXISTS Subcategory;

CREATE TABLE Subcategories(
    id_subcategory SMALLINT(5) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    subcategory_name VARCHAR(40),
    category_id SMALLINT(5) UNSIGNED,
    product_id SMALLINT(5) UNSIGNED,
    KEY fk_subcategory_id(category_id),
    KEY fk_product_id(product_id),
    CONSTRAINT fk_subcategory_id FOREIGN KEY(category_id) REFERENCES Categories(id_category),
    CONSTRAINT fk_product_id FOREIGN KEY(product_id) REFERENCES Product(id_product)
)engine=InnoDB
DEFAULT CHARACTER SET = utf8;

SELECT * from product INNER JOIN categories on categories.id_category = product.category_id INNER JOIN subcategories ON subcategories.category_id=categories.id_category;


DROP TABLE Product;
DROP TABLE Replaced_product;
DROP TABLE Subcategory:
DROP TABLE Nutrition_data;
DROP TABLE Categories;
