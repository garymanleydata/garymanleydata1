CREATE VIEW current_period AS
SELECT
	202202 period
;
 
select user(), session_user(), CURRENT_TIMESTAMP() ;
select * from current_period; 

DROP TABLE ice_control;

-- ICE_CONTROL
CREATE TABLE ice_control 
(
control_id NUMERIC, 
control_desc varchar(200), 
amended_user_id varchar(200), /*needs a trigger to look into*/
amended_date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
CONSTRAINT ice_cont_pk PRIMARY KEY (control_id) 
) ;

DELETE
FROM
	ice_control ;

INSERT
	INTO
	ice_control (control_id,
	control_desc)
	-- amended_user_id, amended_date_time) 
VALUES (1,
		'Gary test script e.g. exercise count' ) ;

INSERT
	INTO
	ice_control (control_id,
	control_desc)
	-- amended_user_id, amended_date_time) 
VALUES (2,
		'Gary test script e.g. crunch count' ) ;

	
COMMIT; 

-- ICE_SOURCE  -- source_id, source_desc, amended_user_id, amended_date_time 
CREATE TABLE ice_source
(
source_id NUMERIC, 
source_desc varchar(200), 
amended_user_id varchar(200), 
amended_date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
CONSTRAINT ice_src_pk PRIMARY KEY (source_id) 
) ;

INSERT
	INTO
	ice_source (source_id,
	source_desc)
VALUES(1,
		'Gary test source e.g. Start ETL' );

INSERT
	INTO
	ice_source (source_id,
	source_desc)
VALUES(2,
	'Gary test source e.g. END ETL' );


-- ICE_CONTROL_SOURCE_LINK -- csl_id, control_id, source_id, sql_text , amended_user_id, amended_date_time , master_ind

-- MySQL is case sensitive
CREATE TABLE ICE_CONTROL_SOURCE_LINK
(
csl_id NUMERIC, 
control_id NUMERIC, 
source_id NUMERIC, 
sql_text varchar(2000),
master_ind char(1) DEFAULT 'N', 
amended_user_id varchar(200), 
amended_date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
CONSTRAINT ic_csl_pk PRIMARY KEY (csl_id) ,
CONSTRAINT ic_csl_src_fk FOREIGN KEY (source_id) REFERENCES ice_source (source_id), 
CONSTRAINT ic_csl_cntl_fk FOREIGN KEY (control_id) REFERENCES ice_control (control_id)
) ;


DELETE
FROM
	ICE_CONTROL_SOURCE_LINK;

INSERT
	INTO
	ICE_CONTROL_SOURCE_LINK (csl_id,
	control_id,
	source_id,
	sql_text,
	master_ind)
VALUES (1,
1,
1,
'select 202202 year_month , 100 amount from dual',
'Y');

INSERT
	INTO
	ICE_CONTROL_SOURCE_LINK (csl_id,
	control_id,
	source_id,
	sql_text,
	master_ind)
VALUES (2,
1,
2,
'select 202202 year_month , 100 amount from dual',
'Y');

INSERT
	INTO
	ICE_CONTROL_SOURCE_LINK (csl_id,
	control_id,
	source_id,
	sql_text,
	master_ind)
VALUES (3,
2,
1,
'select 202202 year_month , 100 amount from dual',
'Y');

SELECT
	*
FROM
	ICE_CONTROL_SOURCE_LINK
;

COMMIT;

SET FOREIGN_KEY_CHECKS = 0;

CREATE TABLE ice_amount
(
year_months numeric, 
csl_id numeric, 
amount numeric, 
latest_ind char(1),
amended_user_id varchar(200) , 
amended_date_time timestamp default current_timestamp,
CONSTRAINT ic_amtcsl_src_fk FOREIGN KEY (csl_id) REFERENCES ice_control_source_link (csl_id)
) 
; 

SET FOREIGN_KEY_CHECKS = 1;

create table ice_control_error 
(
icsl_id numeric , 
year_months numeric, 
amended_user_id varchar(200), 
amended_date_time timestamp default current_timestamp
); 

/*I have created the tables, now to look at procedures!*/

