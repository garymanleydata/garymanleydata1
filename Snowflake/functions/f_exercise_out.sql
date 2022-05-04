create or replace function f_exercise_out(p_daily_total number, p_avg number, p_std number , p_coeff number)
returns varchar2(1)
as
$$
select case when p_daily_total = 0 then 'L' 
            when p_daily_total < (p_avg - (p_std*p_coeff)) THEN 'L'
            when p_daily_total > (p_avg + (p_std*p_coeff)) THEN 'U'
            else 'W'
            END  
$$
;