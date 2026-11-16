export const headers=['需求编号','产品名称','品牌','完整型号','需求数量','计量单位','收货国家/地区','收货城市','期望到货日期','规格补充','接受替代品','其他采购要求'];
const num=x=>typeof x==='number'&&Number.isFinite(x);
export function evaluate(r,q){
 const reasons=[];
 for(const [k,label] of [['exact','型号/关键规格未确认完全匹配'],['original_verified','全新原装待核验'],['conditions_met','配送/交期/其他采购条件待确认']]) if(q[k]!==true) reasons.push(label);
 const pack=q.pack_units;
 if(!num(pack)||pack<=0) reasons.push('包装换算未知');
 if(!num(q.stock_packs)||q.stock_packs<0||!num(pack)||q.stock_packs*pack<r.quantity) reasons.push('库存未知或不足');
 if(!num(q.moq_packs)||q.moq_packs<0||!num(pack)||q.moq_packs*pack>r.quantity) reasons.push('起订量未知或不满足');
 const packs=r.quantity/pack;
 if(!num(q.multiple_packs)||q.multiple_packs<=0||!Number.isFinite(packs)||Math.abs(packs/q.multiple_packs-Math.round(packs/q.multiple_packs))>1e-8) reasons.push('购买倍数未知或不满足');
 if(!q.evidence||!q.url||!q.checked_at) reasons.push('缺少来源/查询时间/判定依据');
 const eligible=!reasons.length;
 let price=null;
 if(num(pack)&&pack>0&&num(q.price_pack)&&q.price_pack>0&&num(q.tier_min_packs)&&q.tier_min_packs>=0&&q.tier_min_packs<=packs&&(q.tier_max_packs==null||(num(q.tier_max_packs)&&packs<=q.tier_max_packs))){
  if(q.currency==='CNY') price=q.price_pack/pack;
  else if(num(q.fx_cny)&&q.fx_cny>0&&q.fx_source&&q.fx_date) price=q.price_pack/pack*q.fx_cny;
 }
 const tax=['含税','未税'].includes(q.tax)?q.tax:'税况未知';
 return {eligible,reasons,price,group:eligible&&price!==null?`人民币参考单价/${tax}`:'不参与价格排名'};
}
export function processTask(task){
 if(!Array.isArray(task.requests)||!task.requests.length) throw Error('缺少需求');
 const ids=new Set();
 for(const r of task.requests){
  if(typeof r.id!=='string'||!r.id.trim()||ids.has(r.id)) throw Error('需求编号缺失或重复，必须使用文本'); ids.add(r.id);
  if(['待补充','待用户确认'].includes(r.status)){
   if(!r.pending_reason)throw Error(`${r.id}: 缺少待确认原因`);
   continue;
  }
  for(const k of ['name','brand','model','unit','country','city']) if(!r[k]) throw Error(`${r.id}: 缺少${k}`);
  if(!num(r.quantity)||r.quantity<=0) throw Error('需求数量必须为正数');
 }
 const seen=new Set(), rows=[];
 for(const q of task.quotes||[]){
  const r=task.requests.find(r=>r.id===q.request_id); if(!r) throw Error('报价关联未知需求');
  if(!['CN','GLOBAL'].includes(q.region)||!q.channel||!/^https?:\/\//.test(q.url||'')||!q.checked_at||!q.evidence) throw Error('报价缺少渠道/地域/有效来源/时间/证据');
  const key=JSON.stringify(Object.keys(q).sort().map(k=>[k,q[k]]));
  if(seen.has(key)) continue; seen.add(key);
  const evaluated=evaluate(r,q);
  if(['待补充','待用户确认'].includes(r.status)){evaluated.eligible=false;evaluated.group='不参与价格排名';evaluated.reasons.push(r.pending_reason);}
  rows.push({...q,...evaluated});
 }
 // Conflicting observations of the same offer remain visible and await reconciliation.
 const offers=new Map();
 for(const q of rows){
  const k=JSON.stringify([q.request_id,q.channel,q.url,q.pack_units,q.tier_min_packs,q.tier_max_packs,q.tax]);
  const group=offers.get(k)||[];group.push(q);offers.set(k,group);
 }
 for(const group of offers.values()){
  const facts=new Set(group.map(q=>JSON.stringify([q.price_pack,q.currency,q.stock_packs,q.moq_packs,q.multiple_packs,q.exact,q.original_verified,q.conditions_met])));
  if(facts.size>1)for(const q of group){q.eligible=false;q.group='不参与价格排名';q.reasons.push('同一报价条件存在冲突记录，待重新核验');}
 }
 const summary=task.requests.map(r=>{
  if(['待补充','待用户确认'].includes(r.status))return {...r,count:0,global_reason:r.pending_reason};
  const c=task.coverage?.[r.id];
  const completed=c=>c?.complete===true&&Array.isArray(c.queries)&&c.queries.length>0&&c.queries.every(x=>typeof x==='string'&&x.trim())&&c.scope&&c.stop_reason;
  if(!completed(c?.mainland)) throw Error(`${r.id}: 大陆覆盖未完成`);
  const domestic=rows.some(q=>q.request_id===r.id&&q.region==='CN'&&q.eligible);
  if(!domestic&&!completed(c.global)) throw Error(`${r.id}: 需要完成全球搜索`);
  const count=rows.filter(q=>q.request_id===r.id&&q.eligible).length;
  return {...r,count,global_reason:domestic?'大陆已有符合条件渠道':'大陆未找到同时满足型号、数量、原装及采购条件的渠道',status:count?'有符合条件渠道':'未找到已核实符合条件渠道'};
 });
 rows.sort((a,b)=>String(a.request_id).localeCompare(String(b.request_id))||Number(b.eligible)-Number(a.eligible)||a.group.localeCompare(b.group)||(a.price??Infinity)-(b.price??Infinity));
 const ranks={}; for(const q of rows) if(q.group!=='不参与价格排名'){const k=JSON.stringify([q.request_id,q.group]);q.rank=ranks[k]=(ranks[k]||0)+1;}
 return {summary,rows};
}
