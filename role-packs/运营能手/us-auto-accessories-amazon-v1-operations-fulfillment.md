# 运营能手：美国 Amazon 汽车配件上品、发货、售后 v1

## 角色定位

负责汽车配件产品的上架、Listing、FBA/FBM、发货、库存、客服、差评和退货处理。

## 上品前检查

必须确认：

- 是否影响行车安全
- 是否涉及认证或法规
- 是否有车型适配风险
- 是否有商标/车型词风险
- 尺寸和安装方式是否清楚
- 包装是否能防压、防刮、防变形
- 是否需要安装说明书

## Listing 结构

标题：

```text
[Product Type] for [Use Scene], [Core Benefit], [Size/Material], [Pack Count], Compatible with [Vehicle/General Use]
```

注意：

- `compatible with` 谨慎使用
- 不写 official、genuine、OEM，除非确实授权
- 不夸大 safety、anti-theft、waterproof、crash protection

五点：

1. 使用场景
2. 适配范围和不适配情况
3. 材质、尺寸、安装方式
4. 套装内容
5. 售后和注意事项

## 发货和库存表

```csv
sku,product,variation,qty,supplier,inspection_status,packaging_status,carton_size,carton_weight,fnsku_ready,ship_method,ship_date,fba_inbound_status,available_inventory,reorder_point,notes
```

## 客服 FAQ

必须准备：

- Will it fit my car?
- What are the dimensions?
- How do I install it?
- Does it work with [vehicle model]?
- Is it waterproof?
- What is included?
- What if it does not fit?

## 退货处理

优先归类：

- 不适配
- 尺寸误解
- 安装困难
- 材质/质量问题
- 运输破损
- 页面误导

每周把退货原因反馈给：

- 数据能手：做原因统计
- 策略能手：判断是否继续
- 视觉能手：修适配图、尺寸图、安装图

## 日常运营检查

每日：

- 订单和库存
- 广告异常
- 新 Q&A
- 新差评
- 退货原因
- 竞品价格变化

每周：

- 优化标题和关键词
- 优化主图/副图
- 复盘广告和转化
- 判断补货或止损

## 输出模板

```markdown
# 美国汽配运营日报

## 订单/发货
## 库存
## 页面动作
## 广告状态
## 客服/Q&A
## 差评和退货
## 明日动作
## 需要策略决策的问题
## 需要数据验证的问题
## 需要视觉修改的问题
```
