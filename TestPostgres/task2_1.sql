with vod as(
	select
		*,
		to_char(report_date, 'YYYY-MM') as mon,
		sum(txn_amount) over(partition by client_id, to_char(report_date, 'YYYY-MM'), txn_type) as operation_amount,
		first_value(vsp_number) over(partition by client_id, to_char(report_date, 'YYYY-MM') order by report_date desc) as last_vsp
	from vsp_oper_data
), cred as (
	select 
		client_id,
		mon,
		operation_amount as credit_amount
	from vod
	where txn_type = 'credit'
	order by client_id
), deb as (
	select 
		client_id,
		mon,
		operation_amount as debit_amount
	from vod
	where txn_type = 'debit'
	order by client_id
)
select distinct 
	vod.client_id, 
	vod.mon as report_date, 
	deb.debit_amount, 
	cred.credit_amount,
	vod.last_vsp
from vod
	full join cred 
		on (cred.client_id = vod.client_id and cred.mon = vod.mon)
	full join deb 
		on (deb.client_id = vod.client_id and deb.mon = vod.mon)

