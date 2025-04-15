USE northwind;

-- -----------------------------------------------------
-- Model Params Table and data added by Dr. Fontenot
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS model1_param_vals(
    sequence_number INTEGER AUTO_INCREMENT PRIMARY KEY,
    beta_0 FLOAT,
    beta_1 FLOAT,
    beta_2 FLOAT
);

INSERT INTO model1_param_vals(beta_0, beta_1, beta_2) values (0.1214, 0.2354, 0.3245);

CREATE TABLE IF NOT EXISTS model1_params(
    sequence_number INTEGER AUTO_INCREMENT PRIMARY KEY,
    beta_vals varchar(100)
);

INSERT INTO model1_params (beta_vals) VALUES ("[0.124, 0.2354, 0.3245]");

commit;
