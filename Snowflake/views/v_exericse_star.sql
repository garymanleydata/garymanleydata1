create or replace view KEBOOLA_7127.WORKSPACE_15661914.V_EXERCISE_STAR as
SELECT timestamp, date_done, description, cast(activity_count as integer) act_count
FROM KEBOOLA_7127.WORKSPACE_15661914.EXERCISE_FACT EF
INNER JOIN KEBOOLA_7127.WORKSPACE_15661914.ACTIVITY_TYPE_DIM ACT ON EF.ACTIVITY_TYPE_ID = ACT.ID
UNION ALL 
select 'N/A',  to_date("Date",'DD/MM/YYYY'), 'Walking' , cast("Steps"/1000 as integer) stepsk
from "gfit_metrics"
 