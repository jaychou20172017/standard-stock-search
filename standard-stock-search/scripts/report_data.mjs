import {processTask} from './core.mjs';
export function buildSheets(mode,task){
 if(mode==='questions'){
  if(!Array.isArray(task.questions)||!task.questions.length)throw Error('缺少待确认问题');
  const ids=new Set();
  for(const q of task.questions){if(!q.issue_id||ids.has(q.issue_id)||!q.request_id||!q.question)throw Error('问题缺少编号、关联产品或问题内容，或编号重复');ids.add(q.issue_id);}
  return [{name:'待确认清单',title:'请填写用户决定后上传',labels:['问题编号','产品编号','源行','问题','可选处理方式','用户决定','状态'],rows:task.questions.map(q=>[q.issue_id,q.request_id,q.source_row,q.question,q.options||'补充信息；保持原条件；暂不处理',null,'待用户确认']),width:22}];
 }
 if(mode!=='report')throw Error('不支持的报告类型');
 const {summary,rows}=processTask(task);
 const fields=[['request_id','需求编号'],['rank','组内排名'],['channel','渠道名称'],['channel_type','渠道类型'],['region','搜索地域'],['brand','展示品牌'],['model','展示型号'],['exact','完全匹配'],['price_pack','包装原价'],['currency','币种'],['pack_units','每包装需求单位数'],['tier_min_packs','阶梯下限/包装'],['tier_max_packs','阶梯上限/包装'],['price','人民币参考单位价'],['stock_packs','库存/包装'],['moq_packs','起订量/包装'],['multiple_packs','购买倍数/包装'],['tax','税费口径'],['shipping','运费'],['origin','发货地'],['lead_time','预计交期'],['original_verified','全新原装核验'],['stock_status','库存核验状态'],['evidence','判定依据'],['url','商品链接'],['authorization_url','授权证据链接'],['checked_at','查询时间'],['group','排名分组'],['eligible','条件满足'],['reasons','待确认/不满足原因'],['fx_cny','汇率'],['fx_source','汇率来源'],['fx_date','汇率日期'],['notes','备注']];
 return [
 {name:'需求汇总',title:'现货搜索需求汇总',labels:['需求编号','产品名称','品牌','型号','需求数量','单位','收货地','交期/规格/其他要求','状态','符合条件渠道数','全球搜索判定'],rows:summary.map(r=>[r.id,r.name,r.brand,r.model,r.quantity,r.unit,`${r.country||'待补充'} ${r.city||'待补充'}`,[r.due,r.spec,r.requirements].filter(Boolean).join('；'),r.status,r.count,r.global_reason]),width:22},
 {name:'渠道报价明细',title:'现货渠道报价明细',labels:fields.map(f=>f[1]),rows:rows.length?rows.map(q=>fields.map(([k])=>k==='checked_at'?'时间：'+q[k]:Array.isArray(q[k])?q[k].join('；'):typeof q[k]==='boolean'?(q[k]?'是':'否'):q[k]??'未知')):[fields.map((_,i)=>i===0?'未找到报价':null)],width:22},
 {name:'查询说明',title:'查询范围与比较口径',labels:['项目','说明'],rows:[['排名口径','各需求、各税费组内按需求数量适用的人民币参考单位价排序；不含未知费用，不等于到岸成本。'],['时效','库存和报价为记录查询时间的公开信息，非供货承诺。未知值不当零。'],...Object.entries(task.coverage||{}).flatMap(([id,c])=>Object.entries(c).map(([stage,v])=>[`${id}/${stage}`,'查询词：'+(v.queries||[]).join('、')+'；范围：'+v.scope+'；停止原因：'+v.stop_reason+'；阻碍：'+(v.obstacles||[]).join('、')]))],width:65}
 ];
}
