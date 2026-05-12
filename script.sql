SET DATESTYLE TO POSTGRES, DMY;
SELECT current_date, current_timestamp;

DROP TABLE IF EXISTS cliente CASCADE;
CREATE TABLE cliente(
	id_cliente int PRIMARY KEY,
	nome_cliente VARCHAR(60) NOT NULL,
	fone_cliente NUMERIC(13),
	email_cliente VARCHAR(50),
	whats_cliente NUMERIC(13),
	sexo_cliente CHAR(2) CHECK(sexo_cliente IN ('M', 'F', 'N/A')),
	CPF_cliente NUMERIC(11) UNIQUE,
	CNPJ_cliente CHAR(14) UNIQUE,
	end_cliente VARCHAR(200)
);
DROP TABLE IF EXISTS pedido CASCADE;
CREATE TABLE pedido(
	id_pedido int PRIMARY KEY,
	id_cliente INTEGER NOT NULL,
	valor_pedido NUMERIC(7,2) NOT NULL,
	prazo_entrega DATE,
	data_pedido DATE NOT NULL,
	descricao_pedido VARCHAR(60),
	status_pedido VARCHAR(50) DEFAULT 'Aguardando',
	FOREIGN KEY(id_cliente) REFERENCES cliente(id_cliente)
);

DROP TABLE IF EXISTS fornecedor CASCADE;
CREATE TABLE fornecedor(
	id_forn int PRIMARY KEY NOT NULL,
	CNPJ_forn CHAR(14) UNIQUE NOT NULL,
	nome_forn VARCHAR(100) NOT NULL,
	tipo_forn VARCHAR(30),
	fone_forn CHAR(13),
	email_forn VARCHAR(50),
	end_forn VARCHAR(255)
);

DROP TABLE IF EXISTS compra CASCADE;
CREATE TABLE compra(
	id_compra int NOT NULL,
	id_forn INTEGER NOT NULL,
	valor_compra NUMERIC(10,2),
	descricao_compra VARCHAR(250),
	data_compra DATE NOT NULL,
	PRIMARY KEY(id_compra),
	FOREIGN KEY(id_forn) REFERENCES fornecedor(id_forn)

);

DROP TABLE IF EXISTS pagamento CASCADE;
CREATE TABLE pagamento(
	id_pagamento int NOT NULL,
	id_pedido INTEGER,
	id_forn INTEGER,
	valor_pagamento NUMERIC(10,2),
	data_pagamento DATE NOT NULL,
	status_pagamento CHAR(1) CHECK(status_pagamento IN ('P','N')),
	PRIMARY KEY(id_pagamento));


select * from cliente
select * from pedido
select * from pagamento
select * from compra


SELECT p.id_pagamento, p.data_pagamento, p.valor_pagamento, p.status_pagamento, COALESCE(c.nome_cliente, f.nome_forn) AS nome FROM pagamento p LEFT JOIN pedido ped ON ped.id_pedido = p.id_pedido LEFT JOIN cliente c ON c.id_cliente = ped.id_cliente LEFT JOIN fornecedor f ON f.id_forn = p.id_forn ORDER BY id_pagamento DESC;