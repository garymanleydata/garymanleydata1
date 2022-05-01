create or replace procedure p_run_control(p_csl_id number) returns number 
language sql as 
   
declare 
  v_sql varchar2(2000);
  v_year_month number(6); 

  begin 

  select period into v_year_month from KEBOOLA_7127.WORKSPACE_15661914.CURRENT_PERIOD cp ;
  select sql_text into v_sql from KEBOOLA_7127.WORKSPACE_15661914.ICE_CONTROL_SOURCE_LINK where csl_id = :p_csl_id; 

  v_sql := 'INSERT INTO KEBOOLA_7127.WORKSPACE_15661914.ICE_AMOUNT(year_month,csl_id,amount) select ' || v_year_month || ' , ' || p_csl_id || ' ,  amount FROM (' || v_sql || ' )  x ' ;
 
  execute immediate v_sql;

  exception
    when other then insert into KEBOOLA_7127.WORKSPACE_15661914.ICE_CONTROL_ERROR(icsl_id, year_month)
                                                                            values(:p_csl_id,:v_year_month) ;

end ;
  
  
call p_run_control(1111);

delete from KEBOOLA_7127.WORKSPACE_15661914.ICE_AMOUNT;

select * from KEBOOLA_7127.WORKSPACE_15661914.ICE_AMOUNT;
select * from KEBOOLA_7127.WORKSPACE_15661914.ICE_CONTROL_ERROR;


