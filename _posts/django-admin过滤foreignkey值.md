title: django-admin过滤foreignkey值
date: November 25, 2015 8:57 PM 
categories: 编程
tags: [Python, Django]

---

### 问题背景
	在用django的admin进行管理的时候，对于指定的用户角色，不希望他看到特定状态的foreignkey，可以采用以下方案。
    当然，也可通过自定义form解决该问题。

### 解决方案

```python
class FactoryOrderItemInline(admin.TabularInline):
    model = FactoryOrderItem
    fields = ('order_item', 'product_sn', 'style', 'size', 'factory_sn', 'price', 'quantity', 'amount')
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'order_item':
            try:
                parent_obj_id = request.resolver_match.args[0]
            except IndexError: #仅在新建状态过滤
                kwargs['queryset'] = OrderItem.objects.filter(order__status='2')
        return super(FactoryOrderItemInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
```