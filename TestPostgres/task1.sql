with trr as (
	select tr.client_id, 
		   tr.report_date as tr_report_date,
		   r.report_date as r_report_date,
		   (tr.txn_amount * r.ccy_rate) as rub_amount
	from rates r
	cross join transactions tr
	where r.ccy_code = 840 
	  AND r.report_date <= tr.report_date 
)
select client_id, tr_report_date as report_date, rub_amount
from (
	select *, LAST_VALUE(r_report_date) over(partition by tr_report_date) as last_r_report_date
	from trr
) filter_trr
where r_report_date = last_r_report_date
