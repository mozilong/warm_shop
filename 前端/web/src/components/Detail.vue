<template>
  <base-page :activation="activation"></base-page>
  <div class="data-cont-wrap w1200">
    <div class="crumb">
      <a href="/">首页</a>
      <span>></span>
      <router-link :to="`/commodity`">所有商品</router-link>
      <span>></span>
      <a href="javascript:;">产品详情</a>
    </div>
    <div class="product-intro layui-clear">
      <div class="preview-wrap">
        <img height="300" width="300" :src="path + commoditys.img">
      </div>
      <div class="itemInfo-wrap">
        <div class="itemInfo">
          <div class="title">
            <h4>{{ commoditys.name }}</h4>
            <span @click="myLike(commoditys.id)"><i class="layui-icon"
                                                    :class="likes ?'layui-icon-rate-solid':'layui-icon-rate'"></i>收藏</span>
          </div>
          <div class="summary">
            <p class="reference"><span>参考价</span>
              <del>￥{{ commoditys.price }}</del>
            </p>
            <p class="activity"><span>活动价</span><strong class="price"><i>￥</i>{{
                commoditys.discount
              }}</strong></p>
            <p class="address-box"><span>送&nbsp;&nbsp;&nbsp;&nbsp;至</span>
              <strong class="address">广东&nbsp;&nbsp;广州&nbsp;&nbsp;天河区</strong>
            </p>
          </div>
          <div class="choose-attrs">
            <div class="color layui-clear"><span class="title">规&nbsp;&nbsp;&nbsp;&nbsp;格</span>
              <div class="color-cont"><span class="btn active">{{ commoditys.sezes }}</span></div>
            </div>
            <div class="number layui-clear"><span class="title">数&nbsp;&nbsp;&nbsp;&nbsp;量</span>
              <div class="number-cont"><span class="cut btn">-</span>
                <input onkeyup="if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}
                                        else{this.value=this.value.replace(/\D/g,'')}"
                       onafterpaste="if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}
                         else{this.value=this.value.replace(/\D/g,'')}" maxlength="4" type="" id="quantity"
                       :value="quantity">
                <span class="add btn">+</span></div>
            </div>
          </div>
          <div class="choose-btns">
            <a class="layui-btn  layui-btn-danger car-btn" @click="addCar(commoditys.id, quantity)">
              <i class="layui-icon layui-icon-cart-simple"></i>加入购物车</a>
          </div>
        </div>
      </div>
    </div>
    <div class="layui-clear">
      <div class="aside">
        <h4>热销推荐</h4>
        <div class="item-list">

          <div class="item" v-for="(r, key) in recommend" :key="key">
            <router-link :to="`/commodity/detail/${r.id}`">
              <img height="280" width="280" :src="path + r.img">
            </router-link>
            <p style="width: 280px;line-height: 25px">
              <span title="{{ r.name }}" >{{ r.name }}</span>
              <span class="pric">￥{{ r.discount }}</span>
            </p>
          </div>

        </div>
      </div>
      <div class="detail">
        <h4>详情</h4>
        <div class="item">
          <img width="800" :src="path + commoditys.details">
        </div>
      </div>
    </div>
  </div>
  <footer-page></footer-page>
</template>

<script>
export default {
  name: "Detail",
  data() {
    return {
      activation: "commodity",
      commoditys: {},
      recommend: [],
      likes: false,
      quantity: 1,
      path: this.$store.state.lookImgUrl
    }
  },
  mounted: function () {
    this.getcode(); //页面加载时自动执行
    // 加载layui的JS脚本，购买数量的加减按钮触发的函数
    window.layui.config({
      base: 'js/'
    }).use(['jquery'], function () {
      var $ = window.layui.$;
      var cur = $('.number-cont input').val();
      $('.number-cont .btn').on('click', function () {
        if ($(this).hasClass('add')) {
          cur++;
        } else {
          if (cur > 1) {
            cur--;
          }
        }
        $('.number-cont input').val(cur)
      })
    })
  },
  methods: {
    // 定义add函数，访问后台获取数据并写入数组myData
    myLike: function (id) {
      this.axios.post('/api/v1/commodity/collect/',
          {id: id}).then(response => {
        if (response.data.state === 'success') {
          this.likes = true
        }
      })
          .catch(function (error) {
            console.log(error)
          })
    },
    addCar: function (id, quantity) {
      if (this.$store.state.username === '') {
        this.$router.push({path: '/shopper/login'})
      }
      this.axios.post('/api/v1/shopper/shopcart/',
          {id: id, quantity: quantity}).then(response => {
        if (response.data.state === 'success') {
          // 加购成功跳转购物车页面
          this.$router.push({path: '/shopper/shopcart/'})
        }
      })
          .catch(function (error) {
            console.log(error)
          })
    },
    getcode: function () {
      this.axios.get('/api/v1/commodity/detail/' + this.$route.params.id).then(response => {
        this.commoditys = response.data.data.commoditys
        this.recommend = response.data.data.recommend
        this.likes = response.data.data.likes
        console.log(this.commoditys)
      })
          .catch(function (error) {
            console.log(error)
          })
    }
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
