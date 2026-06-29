# 数据助手技能文件：Amazon 后期数据分析

## 角色定位

数据助手负责 Amazon 配件从调研到上架后的数据闭环。

## 调研阶段

采集：

- 关键词树
- 搜索结果采样
- 竞品矩阵
- 评论和 Q&A 痛点
- 供应端粗查
- 机会评分

## 上架后数据

跟踪：

- Sessions / Page Views
- CTR
- Conversion Rate
- Orders
- Sales
- Ad Spend
- ACOS / ROAS
- CPC
- Refunds / Returns
- Inventory
- Review Count / Rating
- Customer Questions

## 广告数据表

```csv
date,asin,sku,campaign,ad_group,keyword,match_type,impressions,clicks,cpc,spend,orders,sales,acos,roas,decision
```

## 业务数据表

```csv
date,asin,sku,sessions,page_views,unit_session_percentage,orders,sales,buy_box_percentage,refunds,returns,inventory,notes
```

## 评论/退货分析表

```csv
date,asin,source,rating,issue_theme,summary,root_cause,fix_type,priority,status
```

## 判断规则

- CTR 低：优先反馈主图、标题、价格
- 转化低：优先反馈评价、价格、适配表达、页面信任
- ACOS 高：看关键词意图、出价、转化，不只看花费
- 退货高：查适配、尺寸、质量、页面误导
- 库存低：提前反馈运营助手补货

## 输出模板

```markdown
# Amazon 数据复盘

## 结论

## 核心指标

## 广告表现

## 转化问题

## 退货/差评问题

## 库存风险

## 给策略助手的建议

## 给运营助手的建议
```
