<template>
    <base-page :activation="activation"></base-page>
    <div class="carts w1200">
        <div class="cart-table-th">
            <div class="th th-chk">
                <div class="select-all">
                    <div class="cart-checkbox">
                        <input class="check-all check" id="allCheckked" type="checkbox" value="true">
                    </div>
                    <label>&nbsp;&nbsp;全选</label>
                </div>
            </div>
            <div class="th th-item">
                <div class="th-inner">商品</div>
            </div>
            <div class="th th-price">
                <div class="th-inner">单价</div>
            </div>
            <div class="th th-amount">
                <div class="th-inner">数量</div>
            </div>
            <div class="th th-sum">
                <div class="th-inner">小计</div>
            </div>
            <div class="th th-op">
                <div class="th-inner">操作</div>
            </div>
        </div>
        <div class="OrderList">
            <div class="order-content" id="list-cont">

                <ul class="item-content layui-clear" v-for="(c, key) in cartInfos" :key="key">
                    <li class="th th-chk">
                        <div class="select-all">
                            <div class="cart-checkbox">
                                <input class="CheckBoxShop check" id=""
                                       type="checkbox" num="all" name="select-all" value="true">
                            </div>
                        </div>
                    </li>
                    <li class="th th-item">
                        <div class="item-cont">
                            <a href="javascript:;"><img :src="path + c.commodityInfos_id.img"></a>
                            <div class="text">
                                <div class="title">{{ c.commodityInfos_id.name }}</div>
                                <p><span>{{ c.commodityInfos_id.sezes }}</span></p>
                            </div>
                        </div>
                    </li>
                    <li class="th th-price">
                        <span class="th-su">{{ c.commodityInfos_id.price }}</span>
                    </li>
                    <li class="th th-amount">
                        <div class="box-btn layui-clear">
                            <div class="less layui-btn" >-</div>
                            <input class="Quantity-input" :value="c.quantity" disabled="disabled">
                            <div class="add layui-btn" >+</div>
                        </div>
                    </li>
                    <li class="th th-sum">
                        <span class="sum">0</span>
                    </li>
                    <li class="th th-op" @click="delCarInfo(c.id)">
                        <span>删除</span>
                        <p hidden="hidden">{{ c.id }}</p>
                    </li>
                </ul>

            </div>
        </div>
        <div class="FloatBarHolder layui-clear">
            <div class="th th-chk">
                <div class="select-all">
                    <div class="cart-checkbox">
                        <input class="check-all check" name="select-all" type="checkbox" value="true">
                    </div>
                    <label>&nbsp;&nbsp;已选<span class="Selected-pieces">0</span>件</label>
                </div>
            </div>
            <div class="th batch-deletion" @click="delCarInfo(username)">
                <span class="batch-dele-btn">删除全部</span>
                <p hidden="hidden" id="userId">{{ username }}</p>
            </div>
            <div class="th Settlement">
                <button class="layui-btn" @click="pays">结算</button>
            </div>
            <div class="th total">
                <p>应付：<span class="pieces-total">￥0.00</span></p>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Shopcart",
        data() {
            return {
                activation: 'shopcart',
                cartInfos: [],
                username: this.$store.state.username,
                path: this.$store.state.lookImgUrl
            }
        },
        beforeMount: function(){
            this.getcode(); //页面加载时自动执行
        },
        updated: function () {
            this.getSum(); //页面更新完成执行JS计算价钱
        },
        methods: {
            getcode () {
                this.axios.get('/api/v1/shopper/shopcart/').then(response => {
                    this.cartInfos = response.data.data
                    this.getSum()
                })
                    .catch(function (error) {
                        console.log(error)
                    })
            },
            pays: function () {
                var d = {'total': window.layui.$(".pieces-total").text()}
                this.axios.post('/api/v1/shopper/pays/', d).then(response => {
                    if (response.data.data !== ''){
                        window.location.href = response.data.data
                    }
                })
                    .catch(function (error) {
                        console.log(error)
                    })
            },
            delCarInfo(style) {
                var d
                if (style === this.username) {
                    d = {username: this.username}
                } else {
                    d = {carId: style}
                }
                this.axios.post('/api/v1/shopper/delete/', d).then(response => {
                    if (response.data.state === 'success') {
                        // 删除成功
                        this.getcode(); //重新加载购物车
                    }
                })
                    .catch(function (error) {
                        console.log(error)
                    })
            },
            getSum: function () {
                window.layui.config({
                    base: 'js/'
                }).use(['jquery', 'element', 'car'], function () {
                    var $ = window.layui.$;
                    var car = window.layui.car;
                    car.init();
                    $(function () {
                        var counts = 0;
                        $(".sum").each(function (i, e) {
                            var quantity = $('.th-su')[i].innerHTML
                            var price = $('.Quantity-input')[i].value
                            e.innerHTML = (quantity * price).toFixed(2)
                            counts = counts * 1 + e.innerHTML * 1
                        });
                        $(".pieces-total").text("￥" + counts.toFixed(2))
                    });
                });
            }
        },
    }
</script>

<style scoped>

</style>
