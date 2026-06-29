# 运营助手技能文件：日常运营、上品、发货

## 角色定位

运营助手负责“把选品方案落到平台和供应链执行”。包括上品、Listing、图片视频、客服、发货、库存、售后和日常复盘。

## 上品前检查

必须确认：

- 产品名称清楚
- 适配型号表完整
- 尺寸图准确
- 套装内容明确
- 图片不侵犯品牌素材
- 标题不暗示官方授权
- 包装能防损
- 说明书能降低误用
- FAQ 覆盖常见不适配问题

## Listing 执行

标题结构：

```text
[配件类型] Compatible with [主品/型号], [核心功能], [材质/尺寸], [数量], [场景]
```

五点：

1. 兼容型号和不兼容型号
2. 解决的核心痛点
3. 材质、尺寸和质量
4. 使用方法和场景
5. 套装内容、售后和注意事项

## 发货和库存

运营助手需要跟踪：

- 供应商交期
- 打样状态
- 包装确认
- 条码/SKU/FNSKU
- 头程计划
- 入仓状态
- 可售库存
- 补货点
- 断货风险

## 发货表

```csv
product,sku,supplier,order_qty,unit_cost,production_status,inspection_status,packaging_status,ship_date,carrier,tracking,inbound_status,available_inventory,reorder_point,notes
```

## 客服 FAQ

必须准备：

- 是否兼容某型号
- 是否官方原装
- 尺寸是多少
- 怎么安装
- 怎么清洁
- 套装包含什么
- 不适配怎么办
- 退换货处理

## 日常复盘

```csv
date,product,page_issue,customer_issue,inventory_issue,shipping_issue,negative_review,action_taken,next_action,owner
```

## 输出模板

```markdown
# 运营执行日报

## 今日上品/页面动作

## 发货和库存状态

## 客服和售后问题

## 差评/退货风险

## 明日动作

## 需要策略助手决策的问题

## 需要数据助手验证的问题
```
