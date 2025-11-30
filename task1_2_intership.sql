select o.id_user, o.id_region, sum(o.amount) as amount, avg_amount_by_region.avg_amount 
from orders o 
join (
	select id_region, avg(amount) as avg_amount 
	from orders 
	where status='success' 
	group by id_region
) avg_amount_by_region on o.id_region = avg_amount_by_region.id_region
where o.status='success'
group by o.id_user, o.id_region, avg_amount_by_region.avg_amount 
having sum(o.amount) > avg_amount_by_region.avg_amount 
order by o.id_region
