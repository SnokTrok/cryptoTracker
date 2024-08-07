create table crypto.token (
	id INTEGER serial primary key,
	"name" VARCHAR(50) not null,
	identifier VARCHAR(10) not null,
	chain VARCHAR(10)
);

create table crypto.token_price_history (
	token_id INTEGER,
	date_open TIMESTAMP without TIME zone not null,
	date_close TIMESTAMP without TIME zone not null,
	price_open Numeric(10,6),
	price_close Numeric(10,6),
	price_high numeric(10,6),
	price_low NUMERIC(10,6),
	volume NUMERIC(15,6),
	num_trades INTEGER,
	constraint fk_token_id foreign key (token_id) references crypto."token" (id) on update cascade on delete cascade,
	constraint token_id_date_open_pk primary key (token_id,date_open)
);