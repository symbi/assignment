import collections
import copy
import sys
import pandas as pd

costs, names, types, attractions, guests= None, None, None, None, None
budget=10000000
df=None
dict_amount_cost_idx={} #type_amount_cost_combination
dict_type_idx=collections.defaultdict(list)

def readfile():
	global costs, names, types, data, attractions, df, dict_type_idx
	df = pd.read_csv("attractions.tsv", sep='\t')
	costs = list(df['cost'])
	names = list(df['name'])
	types = list(df['type'])
	attractions = list(df['est_cust'])

	for i,t in enumerate(types):
		dict_type_idx[t].append(i)

#get subset of combinations
def get_subset(arr,sidx,tmp,limit,n,res):
	if len(tmp)==limit:
		res.append(tmp)
		return
	for i in range(sidx,n):
		get_subset(arr,i+1,tmp+[arr[i]],limit,n,res)

#create a dictionary for each type
#sort by attraction amount with all the combinations
def sort_amount_by_type(cd):
	for k,lst_idx in dict_type_idx.items():
		n=len(lst_idx)
		lst_subset=[]
		res = []
		if cd[k]>1:
			get_subset(lst_idx,0,[],cd[k],n,lst_subset)
			for l in lst_subset:
				t_amount=0
				t_cost=0
				for i in l:
					t_amount+=attractions[i]
					t_cost+=costs[i]
				res.append((t_amount,t_cost,l))
		else:
			for i in lst_idx:
				res.append((attractions[i],costs[i],[i]))

		res.sort(key=lambda x: x[0], reverse=1)
		res_d=[]
		i,j=0,1
		while i<len(res):
			res_d.append(res[i])
			while j<len(res) and res[j][1]>res[i][1]:
				j+=1
			i=j
			j=i+1
		dict_amount_cost_idx[k] = res_d


def reduce_to_budget():

	limit=[]#len limit of each type
	p = {'kids': 0, 'food': 0, 'shop': 0, 'coaster': 0, 'flat': 0}
	for k,lst in dict_amount_cost_idx.items():
		limit.append(len(lst))
	max_amount_cost=sys.maxsize
	p_ret=None
	all_types=list(dict_amount_cost_idx.keys())

	while max_amount_cost>budget:
		cp=[]
		ck=[]
		c_amount=0
		c_cost=0
		for k, lst in dict_amount_cost_idx.items():
			cp.append(p[k])
			i=p[k]
			ck.append(lst[i][1]/lst[i][0])
			i=p[k]
			c_amount+=lst[i][0]
			c_cost+=lst[i][1]

		max_amount=c_amount
		max_amount_cost=c_cost
		p_ret=p.copy()
		p_idx_move=ck.index(max(ck))
		if cp[p_idx_move]+1<limit[p_idx_move]:
			type_to_move=all_types[p_idx_move]
			p[type_to_move]+=1


	ret = {}
	for k, lst in dict_amount_cost_idx.items():
		ret[k] = lst[p_ret[k]][2]


	return max_amount,max_amount_cost,p_ret,ret


def add_to_budget(p_old,totalamount,totalcost):

	p_new={}
	for k,v in p_old.items():
		p_new[k]=p_old[k]-1 if p_old[k]>=1 else 0

	all_types=list(dict_amount_cost_idx.keys())
	stop = {'kids': 0, 'food': 0, 'shop': 0, 'coaster':0 , 'flat': 0}

	while True:
		ck=[]
		dif_cost=[]
		dif_amount=[]
		for k,lst in dict_amount_cost_idx.items():
			i=p_new[k]
			j=p_old[k]
			if i==j or stop[k]:
				stop[k]=1
				ck.append(-1)
				dif_cost.append(0)
				dif_amount.append(0)
				continue

			ck.append(lst[i][1]/lst[i][0])
			dif_cost.append(lst[i][1]-lst[j][1])
			dif_amount.append(lst[i][0]-lst[j][0])
		p_idx_to_move=ck.index(max(ck))
		if sum(ck)==-5:break

		if dif_cost[p_idx_to_move]+totalcost<=budget:
			p_old[all_types[p_idx_to_move]]=p_new[all_types[p_idx_to_move]]
			totalcost+=dif_cost[p_idx_to_move]
			totalamount+=dif_amount[p_idx_to_move]
		if p_new[all_types[p_idx_to_move]] - 1 >= 0:
			p_new[all_types[p_idx_to_move]]-=1
		else:
			stop[all_types[p_idx_to_move]]=1



	ret = {}
	for k, lst in dict_amount_cost_idx.items():
		ret[k] = lst[p_old[k]][2]

	return totalamount,totalcost,ret



def get_attractions_from_ret(ret):
	select = []
	attraction_num = 0
	totalcost=0
	for k, v in ret.items():
		select.extend(v)
		for x in v:
			attraction_num += attractions[x]
			totalcost+=costs[x]
	print(df.iloc[select])
	print(select, "guests:", attraction_num,", totalcost:",totalcost)
	return attraction_num,totalcost

if __name__ =="__main__":
	# four conditions
	cd1 = {'kids': 3, 'food': 2, 'shop': 1, 'coaster': 2, 'flat': 2}
	cd2 = {'kids': 3, 'food': 2, 'shop': 1, 'coaster': 3, 'flat': 1}
	cd3 = {'kids': 2, 'food': 2, 'shop': 1, 'coaster': 2, 'flat': 3}
	cd4 = {'kids': 2, 'food': 2, 'shop': 1, 'coaster': 3, 'flat': 2}
	#--prepare--
	readfile()
	#-------
	condition=[cd1,cd2,cd3,cd4]
	amounts=[]
	rets=[]
	for i,cd in enumerate(condition):
		sort_amount_by_type(cd)
		#get maximize attractions then reduce to budget with maximum cost/amount
		amount,cost,p,r=reduce_to_budget()
		#add back to budget with maximum cost/amount
		amount,cost,r=add_to_budget(p,amount,cost)
		amounts.append(amount)
		rets.append(r)
		print("condition",(i+1),":",cd)
		print("max attraction:",amount,", with cost:",cost)
	ret_idx=amounts.index(max(amounts))
	ret_answer=rets[ret_idx]


	print("answer for max attraction is condition",ret_idx+1)
	print(condition[ret_idx])
	get_attractions_from_ret(ret_answer)