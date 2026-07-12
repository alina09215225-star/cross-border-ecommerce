# 运营能手：美国汽配大单品 B站批量学习 v3

## 来源

本技能包来自 10 个 B站课程/视频，重点沉淀汽配上品、车型适配、SKU 组合、售后和 Listing 落地。

## 运营核心

汽配运营的重点不是把一个产品页面做漂亮，而是：

```text
车型适配准确
  ↓
SKU 数据完整
  ↓
页面降低误买
  ↓
履约和售后可控
  ↓
按数据加减法
```

## 上品前检查

```csv
sku,product_type,vehicle_make,vehicle_model,year_range,install_position,oe_number,package_content,images_ready,install_guide,fitment_data,inventory,shipping_method,risk_level
```

必须确认：

- 车型、年份、版本。
- OE 号或替换编号。
- 安装位置。
- 包装内容。
- 是否需要 ACES/车型适配。
- 是否可在标题/五点里合规表达。
- 是否含未授权品牌词、车标或 OEM 风险。

## SKU 组合

课程反复验证：汽配靠 SKU 覆盖，不是单 SKU 取胜。

运营动作：

- 同一产品类型按车型/年份扩 SKU。
- 同一车型按使用场景扩 SKU。
- 同一类目按套装/单件扩 SKU。
- 每周看订单、退货、客服，砍掉低效 SKU。

## Listing 要点

标题：

```text
[Product Type] Compatible with [Make Model Year], [Install Position], [Feature], [Pack/Material]
```

五点：

1. 适配范围。
2. 不适配提醒。
3. 安装步骤。
4. 套装内容。
5. 售后和注意事项。

严禁：

- 未授权写 official / genuine / OEM。
- 误导性使用品牌和车标。
- 隐藏不适配条件。
- 安全性能夸大。

## 售后和退货

记录：

```csv
date,sku,asin,issue_type,vehicle_model,customer_question,return_reason,refund_or_replacement,cost,next_action
```

归类：

- 不适配。
- 安装不会。
- 尺寸/孔位不对。
- 包装损坏。
- 质量缺陷。
- 页面误导。

动作：

- 不适配：补适配表和不适配图。
- 安装不会：补安装图和视频。
- 包装损坏：改包装或暂停补货。
- 高退货低利润：提交下架。

## 加减法

加码：

- 有曝光、有点击、有订单。
- 退货低。
- 客服少。
- 可以扩车型/SKU。
- 利润稳定。

下架：

- 30 天无有效订单。
- 有订单但退货高。
- 客服问题集中在不适配。
- 低价促销仍无利润。
- 需要高风险承诺才能卖。

## 输出模板

```markdown
# 汽配运营执行报告

## 今日上品
## 车型适配
## Listing 修改
## 库存/发货
## 客服和退货
## 加码 SKU
## 下架 SKU
## 需要数据验证
## 需要视觉修改
## 需要策略决策
```
