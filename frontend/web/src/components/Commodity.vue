<template>
    <base-page :activation="activation"></base-page>
    <div class="commod-cont-wrap">
        <div class="commod-cont w1200 layui-clear">
            <div class="left-nav">
                <div class="title">商品分类</div>
                <div class="list-box">
                    <dl v-for="(t, key) in typesList" :key="key">
                        <dt>{{t.name}}</dt>
                        <dd v-for="(s, key) in t.value" :key="key">
                            <router-link :to="{ path: '/commodity', query: { types: s,
                                            search:this.$route.query.search, page: 1,
                                            sort: this.$route.query.sort }}">{{s}}
                            </router-link>
                        </dd>
                    </dl>
                </div>
            </div>
            <div class="right-cont-wrap">
                <div class="right-cont">
                    <div class="sort layui-clear">
                        <router-link :class="this.$route.query.sort == 'sold' ?'active':''"
                                     :to="{ path: '/commodity', query: { types: this.$route.query.types,  search:this.$route.query.search, sort: 'sold'}}">
                            销量
                        </router-link>
                        <router-link :class="this.$route.query.sort == 'price' ?'active':''"
                                     :to="{ path: '/commodity', query: { types: this.$route.query.types,  search:this.$route.query.search, sort: 'price'}}">
                            价格
                        </router-link>
                        <router-link :class="this.$route.query.sort == 'created' ?'active':''"
                                     :to="{ path: '/commodity', query: { types: this.$route.query.types,  search:this.$route.query.search, sort: 'created'}}">
                            新品
                        </router-link>
                        <router-link :class="this.$route.query.sort == 'likes' ?'active':''"
                                     :to="{ path: '/commodity', query: { types: this.$route.query.types,  search:this.$route.query.search, sort: 'likes'}}">
                            收藏
                        </router-link>
                    </div>
                    <div class="prod-number">
                        <a href="javascript:;">商品列表</a>
                        <span>></span>
                        <a href="javascript:;">共{{ count }}件商品</a>
                    </div>
                    <div class="cont-list layui-clear" id="list-cont">

                        <div class="item" v-for="(c, key) in commodityInfos" :key="key">
                            <div class="img">
                                <router-link :to="`/commodity/detail/${c.id}`">
                                    <img height="280" width="280" :src="path + c.img"></router-link>
                            </div>
                            <div class="text">
                                <p class="title">{{ c.name }}</p>
                                <p class="price">
                                    <span class="pri">￥{{ c.price }}</span>
                                    <span class="nub">{{ c.sold }}付款</span>
                                </p>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
            <div id="demo0" style="text-align: center;">
                <div class="layui-box layui-laypage layui-laypage-default" id="layui-laypage-1">
                    <router-link class="layui-laypage-prev" v-if="previous > 0"
                                 :to="{ path: '/commodity', query: { types: this.$route.query.types,
                                 sort:this.$route.query.sort, page:previous, search: this.$route.query.search}}">上一页
                    </router-link>
                    <a v-if="previous <= 0" class="layui-laypage-next">上一页</a>
                    <router-link v-if="previous > 0" :to="{ path: '/commodity', query: { types: this.$route.query.types,
                                sort:this.$route.query.sort, page:previous, search: this.$route.query.search}}">
                        {{previous}}
                    </router-link>


                    <span class="layui-laypage-curr"><em
                            class="layui-laypage-em"></em><em>{{ current ? current : 1 }}</em></span>


                    <router-link v-if="pageCount >= next && current < pageCount"
                                 :to="{ path: '/commodity', query: { types: this.$route.query.types,
                                 sort:this.$route.query.sort, page:next, search: this.$route.query.search}}">{{next}}
                    </router-link>
                    <a v-if="pageCount < next">{{next}}</a>
                    <router-link class="layui-laypage-next" v-if="pageCount >= next"
                                 :to="{ path: '/commodity', query: { types: this.$route.query.types,
                                 sort:this.$route.query.sort, page:next, search: this.$route.query.search}}">下一页
                    </router-link>
                    <a v-if="pageCount < next" class="layui-laypage-next">下一页</a>
                </div>
            </div>
        </div>
    </div>
    <footer-page></footer-page>
</template>

<script>
    export default {
        name: "Commodity",
        data() {
            return {
                activation: "commodity",
                typesList: [{}],
                count: 0,
                next: 0,
                current: 1,
                pageCount: 0,
                previous: 0,
                commodityInfos: [],
                path: this.$store.state.lookImgUrl
            }
        },
        mounted: function () {
            this.getcode(); //页面加载时自动执行
        },
        methods: {

            getcode: function () {
                // 如果当前参数page不等于undefined，说明参数page存在，将其赋值给变量current
                if (typeof (this.$route.query.page) != "undefined") {
                    this.current = this.$route.query.page
                }
                this.axios.get('/api/v1/commodity/list/',
                    {
                        params: {
                            search: this.$route.query.search,
                            sort: this.$route.query.sort,
                            types: this.$route.query.types,
                            page: this.current,
                        }
                    }
                ).then(response => {
                    this.typesList = response.data.data.types
                    this.commodityInfos = response.data.data.commodityInfos.data
                    this.count = response.data.data.commodityInfos.count
                    this.previous = response.data.data.commodityInfos.previous
                    this.next = response.data.data.commodityInfos.next
                    this.pageCount = response.data.data.commodityInfos.pageCount
                    console.log(this.commodityInfos)
                })
                    .catch(function (error) {
                        console.log(error)
                    })
            },
        },
        watch: {
            "$route.query": function () {
                this.getcode()
            }
        }
    }
</script>

<style scoped>

</style>
