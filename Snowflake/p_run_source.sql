create or replace procedure p_run_source(p_source_id number) returns number 
language sql as 

begin 
-- can I declare the cursor directly? and can they go in the declare block
  LET res RESULTSET := (select csl_id as id
                        from KEBOOLA_7127.WORKSPACE_15661914.ICE_CONTROL_SOURCE_LINK 
                        where source_id = :p_source_id
                       );
  LET c1 CURSOR for res;
  LET numtest number default 0;

FOR record in c1 DO
    numtest := record.id;
    call p_run_control(:numtest);
END FOR;
return numtest;
end ;
