-- Set schema to use, saves alias on every script
USE KEBOOLA_7127.WORKSPACE_15661914; 
-- Snowflake Deploy Script 
CREATE VIEW current_period AS
SELECT
	202202 period
FROM
	dual;
    
select * from current_period; 

-- ICE_CONTROL
CREATE TABLE ice_control 
(
control_id NUMBER, 
control_desc varchar2(200), 
amended_user_id varchar2(200) DEFAULT CURRENT_USER(), 
amended_date_time TIMESTAMP DEFAULT  to_timestamp_ntz(current_timestamp),
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
source_id NUMBER, 
source_desc varchar2(200), 
amended_user_id varchar2(200) DEFAULT CURRENT_USER(), 
amended_date_time TIMESTAMP DEFAULT  to_timestamp_ntz(current_timestamp),
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
CREATE TABLE ICE_CONTROL_SOURCE_LINK
(
csl_id NUMBER, 
control_id NUMBER, 
source_id NUMBER, 
sql_text varchar(2000),
master_ind char(1) DEFAULT 'N', 
amended_user_id varchar2(200) DEFAULT CURRENT_USER(), 
amended_date_time TIMESTAMP DEFAULT  to_timestamp_ntz(current_timestamp),
CONSTRAINT ic_csl_pk PRIMARY KEY (csl_id) ,
CONSTRAINT ic_csl_src_fk FOREIGN KEY (source_id) REFERENCES ice_source (source_id), 
CONSTRAINT ic_csl_cntl_fk FOREIGN KEY (control_id) REFERENCES ice_control (control_id)
) ;


DELETE
FROM
	ice_control_source_link;

INSERT
	INTO
	ice_control_source_link (csl_id,
	control_id,
	source_id,
	sql_text,
	master_ind)
VALUES (1,
1,
1,
'select 202202 year_month , 100 amount',
'Y');


INSERT
	INTO
	ice_control_source_link (csl_id,
	control_id,
	source_id,
	sql_text,
	master_ind)
VALUES (2,
1,
2,
'select 202202 year_month , 100 amount',
'Y');

INSERT
	INTO
	ice_control_source_link (csl_id,
	control_id,
	source_id,
	sql_text,
	master_ind)
VALUES (3,
2,
1,
'select 202202 year_month , 100 amount',
'Y');

SELECT
	*
FROM
	ice_control_source_link
;

COMMIT;

-- ICE_AMOUNT -- year_month, csl_id, amount  
CREATE TABLE ice_amount
(
year_month number(6), 
csl_id number, 
amount number, 
latest_ind char(1),
amended_user_id varchar2(200) DEFAULT CURRENT_USER(), 
amended_date_time TIMESTAMP DEFAULT  to_timestamp_ntz(current_timestamp),
CONSTRAINT ic_amtcsl_src_fk FOREIGN KEY (csl_id) REFERENCES ice_control_source_link (csl_id)
) 

; 

create table ice_control_error 
(
icsl_id number , 
year_month number(6), 
amended_user_id varchar2(200) DEFAULT CURRENT_USER(), 
amended_date_time TIMESTAMP DEFAULT  to_timestamp_ntz(current_timestamp)
); 


