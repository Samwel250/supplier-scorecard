# Reads data.json (made by generate_data.py) and writes the static dashboard page index.html.
# Run: python3 make_dashboard.py
import json
d=json.load(open("data.json"));sc=d["sc"];tr=d["tr"]
rows="".join(f'<tr><td>{s["overall_rank"]}</td><td>{s["supplier_name"]}<small>{s["category"]}</small></td><td>{s["delivery_score"]}</td><td>{s["quality_score"]}</td><td>{s["price_score"]}</td><td><div class=bar><i style="width:{s["weighted_score"]}%"></i><b>{s["weighted_score"]}</b></div></td><td><span class="t {s["tier"][0]}">{s["tier"]}</span></td></tr>' for s in sc)
pts=" ".join(f'{i*100/(len(tr)-1):.1f},{100-(v-60)*2.5:.1f}' for i,(m,v) in enumerate(tr))
rev=[s for s in sc if s["tier"]=="Under Review"]
tot=sum(s["total_spend"] for s in sc);rs=sum(s["total_spend"] for s in rev)
ot=sum(s["on_time_rate"]*s["total_orders"] for s in sc)/sum(s["total_orders"] for s in sc)*100
html=f'''<!DOCTYPE html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover"><title>Supplier Performance Scorecard</title><style>
:root{{box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px);--bg:#f6f7f9;--c:#fff;--t:#1b2430;--m:#6b7685;--a:#2563eb;--l:#e3e7ec}}
@media(prefers-color-scheme:dark){{:root:not([data-theme=light]){{--bg:#12161c;--c:#1b212a;--t:#e8ecf1;--m:#9aa5b4;--a:#5b8def;--l:#2b3340}}}}
html{{scroll-padding-top:env(safe-area-inset-top,0px)}}body{{margin:0;padding:16px;background:var(--bg);color:var(--t);font:14px system-ui,sans-serif}}
h1{{font-size:20px;margin:0 0 4px}}p.s{{color:var(--m);margin:0 0 14px}}.g{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-bottom:12px}}
.k,.p{{background:var(--c);border:1px solid var(--l);border-radius:10px;padding:12px}}.k b{{display:block;font-size:22px}}.k span{{color:var(--m);font-size:12px}}
.p{{margin-bottom:12px;overflow-x:auto}}h2{{font-size:14px;margin:0 0 8px}}table{{width:100%;border-collapse:collapse;min-width:560px}}th,td{{text-align:left;padding:7px 6px;border-bottom:1px solid var(--l)}}th{{color:var(--m);font-weight:500;font-size:12px}}
small{{display:block;color:var(--m);font-size:11px}}.bar{{position:relative;background:var(--l);border-radius:5px;height:20px;min-width:120px}}.bar i{{display:block;height:100%;background:var(--a);border-radius:5px}}.bar b{{position:absolute;right:6px;top:2px;font-size:12px}}
.t{{padding:2px 8px;border-radius:99px;font-size:12px}}.P{{background:#d1fae5;color:#065f46}}.A{{background:#fef3c7;color:#92400e}}.U{{background:#fee2e2;color:#991b1b}}svg{{width:100%;height:120px}}</style></head><body>
<h1>Supplier Performance Scorecard &amp; Ranking</h1><p class=s>Simulated procurement data · 12 suppliers · 1,320 POs · Jan 2025–Jun 2026 · Weights: Delivery 40% / Quality 35% / Price 25%</p>
<div class=g><div class=k><span>Overall on-time rate</span><b>{ot:.1f}%</b></div><div class=k><span>Total spend</span><b>${tot/1e6:.1f}M</b></div><div class=k><span>Suppliers under review</span><b>{len(rev)}</b></div><div class=k><span>Spend with review suppliers</span><b>{rs/tot*100:.1f}%</b></div></div>
<div class=p><h2>Ranked scorecard</h2><table><tr><th>#<th>Supplier<th>Delivery<th>Quality<th>Price<th>Weighted score<th>Tier</tr>{rows}</table></div>
<div class=p><h2>Monthly on-time delivery % (all suppliers)</h2><svg viewBox="0 0 100 100" preserveAspectRatio=none><polyline fill=none stroke="var(--a)" stroke-width=1.5 vector-effect=non-scaling-stroke points="{pts}"/></svg></div>
</body></html>'''
open("index.html","w").write(html)
