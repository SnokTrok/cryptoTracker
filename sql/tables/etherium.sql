	CREATE TABLE crypto.ethereum_transaction_history (
	    id SERIAL PRIMARY KEY,
	    block_id BIGINT,
	    from_id BIGINT,
	    to_id BIGINT,
	    amount VARCHAR(200),
	    sent_at TIMESTAMP WITHOUT TIME ZONE,
	    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
	    transaction_number Integer not null,
	    constraint fk_block_id foreign key (block_id) references ethereum_transaction_blocks (id) on update cascade on delete cascade,
	    CONSTRAINT fk_from_id FOREIGN KEY (from_id) REFERENCES user_info(id) ON UPDATE CASCADE ON DELETE CASCADE,
	    CONSTRAINT fk_to_id FOREIGN KEY (to_id) REFERENCES user_info(id) ON UPDATE CASCADE ON DELETE CASCADE
	);
	;
	
	
	create table crypto.ethereum_transaction_blocks (
		id SERIAL primary key,
		block_hash VARCHAR(200) not null,	
		block_number INTEGER not null,
		block_index INTEGER not null,
		block_time TIMESTAMP without TIME zone,
		transaction_count INTEGER not null,
		gas_limit VARCHAR(200) not null,
		gas_used VARCHAR(200) not null,
		"size_bytes" VARCHAR(200) not null,
		miner_id BIGINT not null,
		constraint fk_miner_id foreign key (miner_id) references user_info(id),
		constraint block_hash_uq unique (block_hash) 
	);