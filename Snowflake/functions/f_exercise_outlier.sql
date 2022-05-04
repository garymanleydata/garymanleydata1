create or replace function f_exercise_outlier(p_daily_total number,p_overallavg number)
returns float
as
$$
select case when p_overallavg <= 0 then 0::FLOAT 
else p_overallavg+(2.99292* p_overallavg/sqrt(p_daily_total))::FLOAT end 
$$;