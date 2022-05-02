-- ORACLE Deploy Script 
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
amended_user_id varchar2(200) DEFAULT USER, 
amended_date_time DATE DEFAULT sysdate,
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
amended_user_id varchar2(200) DEFAULT USER, 
amended_date_time DATE DEFAULT sysdate,
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
amended_user_id varchar2(200) DEFAULT USER, 
amended_date_time DATE DEFAULT sysdate,
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
'select 202202 year_month , 100 amount from dual',
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
'select 202202 year_month , 100 amount from dual',
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
'select 202202 year_month , 100 amount from dual',
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
amended_user_id varchar2(200) default user, 
amended_date_time date default sysdate,
CONSTRAINT ic_amtcsl_src_fk FOREIGN KEY (csl_id) REFERENCES ice_control_source_link (csl_id)
) 
--- note this could be a monthly partitioned table 
; 

create table ice_control_error 
(
icsl_id number , 
year_month number(6), 
amended_user_id varchar2(200) default user, 
amended_date_time date default sysdate
); 


-- sample data 
--- have a SQL compilation check 
----- package need to start with run control and store in database 
----- and have a check control is valid 



create or replace package interface_control_environment IS 

  PROCEDURE p_verify_checks(
      p_source_id   NUMBER ,
      p_control_id NUMBER );

  PROCEDURE p_run_source(
      p_source_id   NUMBER, 
      p_mode VARCHAR2 
      );
      
  PROCEDURE p_run_control(
      p_csl_id   NUMBER) ;
     
END interface_control_environment;
/


create or replace package body interface_control_environment

IS 

  PROCEDURE p_verify_checks(p_source_id NUMBER , p_control_id NUMBER ) AS
      
  v_sql varchar2(2000);
  v_icsl_id number; 
  v_year_month number(6); 

  begin 

-- check the controls are valid for a source 
  select period into v_year_month from manle.CURRENT_PERIOD cp ;
  select sql_text, csl_id  into v_sql , v_icsl_id from manle.ice_control_source_link where Source_Id = p_source_id and control_id = p_control_id; 

  v_sql := 'explain plan for ' || v_sql ;

  execute immediate v_sql;

  exception 
    when others then insert into ice_control_error(icsl_id, year_month)values(v_icsl_id,v_year_month) ;
    COMMIT;

  end p_verify_checks;
  
  
  ------ run all the controls for a source
  PROCEDURE p_run_source( p_source_id NUMBER,  p_mode VARCHAR2) AS
  
  cursor c_controls is 
    select csl_id, control_id, source_id from ice_control_source_link where source_id = p_source_id; 
  
  BEGIN 
  
  FOR r_conts in c_controls LOOP
      IF p_mode = 'V' THEN p_verify_checks(p_source_id => r_conts.source_id,p_control_id =>  r_conts.control_id);
                       ELSE p_run_control(p_csl_id => r_conts.csl_id);
      END IF;
  END LOOP;
  
  END p_run_source;


  PROCEDURE p_run_control(p_csl_id NUMBER ) AS
      
  v_sql varchar2(2000);
  v_icsl_id number; 
  v_year_month number(6); 

  begin 

-- check the controls are valid for a source 
  select period into v_year_month from manle.CURRENT_PERIOD cp ;
  select sql_text into v_sql from manle.ice_control_source_link where csl_id = p_csl_id; 

  v_sql := 'INSERT INTO ICE_AMOUNT(year_month,csl_id,amount) select ' || v_year_month || ' , ' || p_csl_id || ' ,  amount FROM (' || v_sql || ' )  x ' ;
 
  execute immediate v_sql;
  
  COMMIT;
 
  exception 
    when others then insert into ice_control_error(icsl_id, year_month)values(v_icsl_id,v_year_month) ;
    COMMIT;

  end p_run_control;
 
 
 
end interface_control_environment ;
/ 

begin
interface_control_environment.p_verify_checks(1,1);
end;
/

begin
interface_control_environment.p_run_source(1,'P');
end;
/

begin
interface_control_environment.p_run_control(1);
end;
/

select * from ice_control_error;

select csl_id, control_id, source_id from ice_control_source_link where source_id = 1; 
SELECT * FROM ICE_AMOUNT;

COMMIT;
