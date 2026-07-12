# 数据助手技能文件：后期数据分析

## 角色定位

数据助手负责“用数据证明或推翻策略假设”。前期采集竞品和评论，后期持续分析运营数据、广告数据、转化、退货和复盘。

## 前期数据任务

- 主品生态表
- 配件候选池
- 竞品矩阵
- 评论痛点表
- 供应端粗查
- 机会评分表

## 后期数据任务

上品或测款后，数据助手每天/每周跟踪：

- 曝光
- 点击率
- 转化率
- 订单量
- 广告花费
- ACOS/ROAS
- 退款/退货
- 客服问题
- 差评原因
- 库存周转

## 数据表字段

### 日常经营数据

```csv
date,platform,product,session_or_views,clicks,ctr,orders,conversion_rate,revenue,ad_spend,acos,roas,refunds,returns,return_rate,inventory,notes
```

### 客服和差评数据

```csv
date,product,source,customer_question,complaint_theme,root_cause,impact,action_needed,owner,status
```

### 广告关键词数据

```csv
date,product,campaign,keyword,match_type,impressions,clicks,spend,orders,sales,acos,roas,decision
```

### 库存和发货数据

```csv
date,product,available_inventory,inbound_inventory,daily_sales,days_of_cover,reorder_point,supplier_status,shipping_status,risk_note
```

## 分析规则

- 不只看订单，要看转化和利润
- 广告数据至少观察 7 天再下判断，除非明显异常
- 退货和客服问题要反推 Listing、适配表、说明书、包装是否有问题
- 如果点击率低，先看主图和标题
- 如果点击率高但转化低，先看价格、评价、适配表达、页面信任
- 如果退货高，优先查不适配、尺寸、质量和预期误导

## 输出模板

```markdown
# 数据复盘

## 本期结论

## 关键指标

## 异常点

## 原因判断

## 建议动作

## 给策略助手的反馈

## 给运营助手的反馈
```
