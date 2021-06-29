CREATE database Login;
use Login;

CREATE table Usuarios (
	id smallint auto_increment primary key,
	Usuario varchar(20) not null,
	`Password` varchar(100) not null,
	unique(Usuario)
);
