<template>
  <div class="header">
    <div class="headerLayout w1200">
      <div class="headerCon">
        <h1 class="mallLogo">
          <a href="/" title="首页">
            <img src="img/logo.png">
          </a>
        </h1>
        <div class="mallSearch">
          <div class="layui-form">
            <input type="text" v-model="search" required lay-verify="required" autocomplete="off"
                   class="layui-input"
                   placeholder="请输入需要的商品">
            <button class="layui-btn" lay-submit lay-filter="formDemo" @click="mySearch">
              <i class="layui-icon layui-icon-search"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="content content-nav-base" :class="activation">
    <div class="main-nav">
      <div class="inner-cont0">
        <div class="inner-cont1 w1200">
          <div class="inner-cont2">
            <router-link :to="`/commodity`" :class="activation == 'commodity' ?'active':''">首页
            </router-link>
            <router-link :to="`/shopper/shopcart`" :class="activation == 'shopcart' ?'active':''">购物车
            </router-link>
            <router-link :to="`/shopper`" :class="activation == 'shopper' ?'active':''">个人中心</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      search: ''
    }
  },
  props: {
    activation: {
      type: String,
      default: ''
    },
  },
  methods: {
    // 搜索商品
    mySearch: function () {
      this.$router.push({path: '/commodity', query: {search: this.search, page: 1}})
    },
  }
}
</script>

<style scoped>

</style>
