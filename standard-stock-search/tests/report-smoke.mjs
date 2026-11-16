// Offline fixture. No supplier or market data.
import fs from 'node:fs/promises';
const dir=process.argv[2];await fs.mkdir(dir,{recursive:true});
const requests=[{id:'001',name:'测试商品（模拟）',brand:'测试品牌',model:'001-A',quantity:20,unit:'个',country:'中国大陆',city:'上海'},{id:'002',name:'零结果商品（模拟）',brand:'测试品牌',model:'002',quantity:1,unit:'套',country:'中国大陆',city:'北京'}];
const c={complete:true,queries:['仅离线模拟'],scope:'模拟数据',stop_reason:'测试结束',checked_at:'2026-10-18T10:00:00+08:00',obstacles:[]};
const quotes=[{request_id:'001',channel:'模拟渠道',channel_type:'模拟授权代理',region:'CN',brand:'测试品牌',model:'001-A',url:'https://example.com/item',checked_at:c.checked_at,evidence:'仅离线测试，不是真实报价',exact:true,original_verified:true,conditions_met:true,pack_units:10,stock_packs:3,moq_packs:1,multiple_packs:1,price_pack:100,currency:'CNY',tier_min_packs:1,tax:'含税',stock_status:'模拟',shipping:'未知',notes:'不得用于采购'}];
await fs.writeFile(dir+'/task.json',JSON.stringify({requests,quotes,coverage:{'001':{mainland:c},'002':{mainland:c,global:c}}}));
