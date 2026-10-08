# Generates the simulated procurement data, loads it into SQLite, runs the scorecard view and exports CSVs.
# Run: python3 generate_data.py
import random, sqlite3, csv, json, datetime as dt
random.seed(26)
# name, category, country, on_time_p, avg_delay_days, defect_mean, price_mult
S=[("Apex Components","Electronics","USA",.96,2,.008,1.04),("Northwind Metals","Raw Materials","Canada",.91,3,.015,.97),
("Pacific Packaging","Packaging","Vietnam",.84,4,.022,.93),("Sterling Plastics","Raw Materials","USA",.93,2,.012,1.02),
("Meridian Circuits","Electronics","Taiwan",.88,3,.018,1.00),("BlueRiver Logistics Supply","MRO","Mexico",.72,6,.030,.95),
("Kestrel Fasteners","MRO","Germany",.95,2,.006,1.10),("Orion Textiles","Packaging","India",.78,5,.045,.90),
("Summit Chemicals","Raw Materials","USA",.89,3,.020,1.06),("Harbor Industrial","MRO","China",.68,7,.052,.88),
("Vertex Electronics","Electronics","Korea",.92,2,.010,1.15),("Lakeside Cartons","Packaging","USA",.86,3,.016,.98)]
db=sqlite3.connect(":memory:"); db.executescript(open("01_schema.sql").read())
sup=[];po=[];pid=1
for i,(n,c,co,otp,dl,dm,pm) in enumerate(S,1):
    sup.append((i,n,c,co))
    for _ in range(random.randint(90,130)):
        od=dt.date(2025,1,1)+dt.timedelta(days=random.randint(0,545)); lead=random.randint(7,30)
        pr=od+dt.timedelta(days=lead)
        late=0 if random.random()<otp else max(1,int(random.gauss(dl*1.8,2)))
        de=pr+dt.timedelta(days=late if late else random.randint(-3,0))
        q=random.randint(100,2000); mk=round(random.uniform(5,120),2)
        up=round(mk*pm*random.uniform(.95,1.05),2)
        d=min(q,int(q*max(0,random.gauss(dm,dm*.5)))); 
        po.append((pid,i,od,pr,de,q,q,d,up,mk)); pid+=1
db.executemany("INSERT INTO suppliers VALUES(?,?,?,?)",sup)
db.executemany("INSERT INTO purchase_orders VALUES(?,?,?,?,?,?,?,?,?,?)",[tuple(str(x) if isinstance(x,dt.date) else x for x in r) for r in po])
db.executescript(open("02_supplier_scorecard.sql").read())
def dump(name,q):
    cur=db.execute(q); cols=[d[0] for d in cur.description]; rows=cur.fetchall()
    csv.writer(open(f"{name}.csv","w",newline="")).writerows([cols]+rows); return cols,rows
dump("suppliers","select * from suppliers"); dump("purchase_orders","select * from purchase_orders")
cols,rows=dump("supplier_scorecard","select * from v_supplier_scorecard order by overall_rank")
sc=[dict(zip(cols,r)) for r in rows]
_,tr=dump("monthly_on_time","SELECT strftime('%Y-%m',order_date) m, ROUND(100.0*SUM(delivery_date<=promised_date)/COUNT(*),1) FROM purchase_orders GROUP BY 1 ORDER BY 1")
_,tier=dump("tier_spend","SELECT tier, ROUND(SUM(total_spend)), ROUND(100.0*SUM(total_spend)/(SELECT SUM(total_spend) FROM v_supplier_scorecard),1) FROM v_supplier_scorecard GROUP BY tier")
json.dump(dict(sc=sc,tr=tr,tier=tier),open("data.json","w"))
print(len(po),"POs");print(tier)
for s in sc: print(s["overall_rank"],s["supplier_name"],s["delivery_score"],s["quality_score"],s["price_score"],s["weighted_score"],s["tier"],round(s["on_time_rate"]*100,1),round(s["defect_rate"]*100,2),round(s["price_index"],2))
print(tr[0],tr[-1])
