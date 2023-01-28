with dm as (
	select vsp, val, group_vsp
	from distance_metric
	union (
		select vsp_e as vsp, val, group_vsp
		from distance_metric
	)
)
select 
	vsp, 
	min(val) as min_val, 
	avg(val)::int as avg_val, 
	max(val) as max_val,
	group_vsp
from dm
group by (vsp, group_vsp)