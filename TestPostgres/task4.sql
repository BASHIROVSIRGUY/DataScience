with up as (
	select 
		*, 
		date(lead(date_position) over(partition by user_id, user_position) - interval '1 day') as inc_date_position,
		date(lag(date_position) over(partition by user_id, user_position) + interval '1 day') as dec_date_position
	from users_position
	order by (user_id, user_position, date_position)
)
select distinct
	user_id,
	user_position,
	case
		when 
			dec_date_position = date_position
		then
			lag(date_position) over(order by (user_id, user_position, date_position))
		else date_position
	end position_start,
	case
		when 
			inc_date_position = date_position
		then
			lead(date_position) over(order by (user_id, user_position, date_position))
		else date_position
	end position_end
from up
