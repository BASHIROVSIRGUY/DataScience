with vod as (
	select 
		client_id, 
		to_char(report_date, 'YYYY-MM') as report_date, 
		count(*) as user_month_debit_count,
		count(*) over (partition by to_char(report_date, 'YYYY-MM')) as month_debit_count
	from vsp_oper_data
	where txn_type = 'debit'
	group by (client_id, to_char(report_date, 'YYYY-MM'))
)
select 
	client_id,
	report_date,
	user_month_debit_count::real / month_debit_count::real as ratio
from vod