from django.core.management.base import BaseCommand
from goods.models import Goods  # 导入商品模型
from faker import Faker  # 用于生成虚拟数据
import random

class Command(BaseCommand):
    help = '生成商品测试数据'

    def handle(self, *args, **options):
        fake = Faker('zh_CN')
        # 商品分类（示例）
        goods_names = [
            "夏季纯棉T恤", "休闲牛仔裤", "透气运动鞋", "超薄笔记本电脑",
            "无线蓝牙耳机", "智能手表", "家用投影仪", "全自动洗衣机",
            "保湿面霜", "男士剃须刀", "进口咖啡豆", "网红零食大礼包"
        ]
        # 批量创建商品
        goods_list = []
        for name in goods_names:
            goods = Goods(
                name=name,
                price=round(random.uniform(29.9, 2999.9), 2),  # 随机价格
                stock=random.randint(10, 1000),  # 随机库存
                status='ON_SALE',  # 状态：在售
                description=fake.text(max_nb_chars=200),  # 随机描述
            )
            goods_list.append(goods)
        # 批量插入数据库
        Goods.objects.bulk_create(goods_list)
        self.stdout.write(self.style.SUCCESS(f'成功生成 {len(goods_list)} 条商品测试数据'))
