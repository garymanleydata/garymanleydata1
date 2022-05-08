select  date_day, 
        year(date_day) date_year, 
        month(date_day) date_month,
        quarter(date_day) date_quarter, 
        DAYOFWEEK( date_day ),
        DAYOFYEAR( date_day ),
        WEEK( date_day ),
        DAYNAME( date_day ),
        date_day -1 lag_date_1, 
        year(date_day)*100+ lpad(month(date_day),2,'0') year_month   
from all_dates
 