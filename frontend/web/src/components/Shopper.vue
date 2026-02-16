<template>
    <base-page :activation="activation"></base-page>
    <div class="info-list-box">
        <div class="info-list">
            <div class="item-box layui-clear">
                <div class="item">
                    <div class="img">
                        <img src="img/portrait.png">
                    </div>
                    <div class="text">
                        <h4>用户：{{ username }}</h4>
                        <p class="data">登录时间：{{ last_login.slice(0,10) }}</p>
                        <div class="left-nav">
                            <div class="title">
                                <router-link :to="`/shopper/shopcart`">我的购物车</router-link>
                            </div>
                            <div class="title" @click="logout"><a>退出登录</a></div>
                        </div>
                    </div>
                </div>
                <div class="item1">
                    <div class="cart">
                        <div class="cart-table-th">
                            <div class="th th-items">
                                <div class="th-inner">
                                    订单编号
                                </div>
                            </div>
                            <div class="th th-price">
                                <div class="th-inner">
                                    订单价格
                                </div>
                            </div>
                            <div class="th th-amount">
                                <div class="th-inner">
                                    购买时间
                                </div>
                            </div>
                            <div class="th th-sum">
                                <div class="th-inner">
                                    订单状态
                                </div>
                            </div>
                        </div>
                        <div class="OrderList">
                            <div class="order-content" id="list-cont">

                                <ul class="item-contents layui-clear" v-for="(o, key) in orders" :key="key">
                                    <li class="th th-items">{{ o.id }}</li>
                                    <li class="th th-price">￥{{ o.price }}</li>
                                    <li class="th th-amount">{{ o.created }}</li>
                                    <li class="th th-sum">{{ o.state }}</li>
                                </ul>

                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </div>
        <div style="text-align: center;">
            <div class="layui-box layui-laypage layui-laypage-default" id="layui-laypage-1">
                <a href="javascript:;" class="layui-laypage-prev">上一页</a>
                <a href="javascript:;">1</a>
                <span class="layui-laypage-curr"><em class="layui-laypage-em"></em><em>2</em></span>
                <a href="javascript:;">3</a>
                <a href="javascript:;" class="layui-laypage-next">下一页</a>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Shopper",
        data() {
            return {
                activation: 'shopper',
                orders: [{}],
                username: this.$store.state.username,
                last_login: this.$store.state.last_login,
            }
        },
        mounted: function () {
            if (this.$store.state.username === '') {
                    this.$router.push({path: '/shopper/login'})
                }
            this.getcode(); //页面加载时自动执行
        },
        methods: {
            getcode: function () {
                var url = '/api/v1/shopper/home/'
                var href = window.location.href.split('?')[1]
                var t = new URLSearchParams('?' + href).get('t')
                if (t !== null){
                    url += '?t=' + t
                }
                console.log(url)
                this.axios.get(url).then(response => {
                    this.orders = response.data.data.orders
                    if (typeof(this.orders) == "undefined") {
                        this.orders = [{}]
                    }
                    console.log(this.orders)
                })
                    .catch(function (error) {
                        console.log(error)
                    })
            },
            logout: function () {
                this.axios.post('/api/v1/shopper/logout/').then(response => {
                    if (response.data.state === 'success') {
                        // 退出登录跳转个人主页
                        this.$store.commit('setUserName','')
                        this.$store.commit('setLastLogin','')
                        console.log(this.state)
                        this.$router.push({path: '/'})
                    }
                })
                    .catch(function (error) {
                        console.log(error)
                    })
            }
        },
    }

</script>

<style scoped>

</style>
