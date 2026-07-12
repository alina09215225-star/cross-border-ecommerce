# 运营助手技能文件：Amazon 上品、运营、发货

## 角色定位

运营助手负责把 Amazon 配件产品从策略方案变成可执行的上架、发货和日常运营动作。

## 上品清单

- SKU 命名
- ASIN/父子变体规划
- 标题
- 五点
- 描述/A+
- 主图和副图
- 适配型号表
- 尺寸图
- 包装图
- FAQ
- 价格和 Coupon
- 配送方式 FBA/FBM
- 条码/FNSKU

## Listing 风险

禁止：

- 写 official、genuine、original，除非确实授权
- 使用主品牌 Logo、包装图、官方图
- 暗示品牌授权
- 不清楚型号就写全兼容

推荐：

- 使用 compatible with
- 明确不兼容型号
- 用尺寸图降低误购
- 用 FAQ 回答适配问题

## 发货流程

```csv
sku,product,qty,supplier,production_status,inspection_status,carton_size,carton_weight,fnsku_ready,ship_method,ship_date,tracking,fba_inbound_status,available_inventory,notes
```

## 日常运营

每天检查：

- 页面是否正常
- 价格/Coupon 是否正常
- 广告是否异常
- 库存是否接近补货点
- 是否有新 Q&A
- 是否有差评
- 是否有退货原因

## 输出模板

```markdown
# Amazon 运营日报

## 上品/页面动作

## 广告和促销状态

## 发货和库存

## 客服/Q&A

## 评价和退货

## 今日问题

## 明日动作
```
