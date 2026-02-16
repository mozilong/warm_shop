<template>
    <base-page :activation="activation"></base-page>
    <div class="login-bg">
        <div class="login-cont w1200">
            <div class="form-box">
                <div class="layui-form">
                    <legend>手机号注册登录</legend>
                    <div class="layui-form-item">
                        <div class="layui-inline iphone">
                            <div class="layui-input-inline">
                                <i class="layui-icon layui-icon-cellphone iphone-icon"></i>
                                <input name="username" id="username" v-model="username"
                                       lay-verify="required|phone" placeholder="请输入手机号"
                                       class="layui-input">
                            </div>
                        </div>
                        <div class="layui-inline iphone">
                            <div class="layui-input-inline">
                                <i class="layui-icon layui-icon-password iphone-icon"></i>
                                <input id="password" type="password" v-model="password"
                                       name="password" lay-verify="required|password"
                                       placeholder="请输入密码" class="layui-input">
                            </div>
                        </div>
                    </div>
                    <p>{{ msg }}</p>
                    <div class="layui-form-item login-btn">
                        <div class="layui-input-block">
                            <button class="layui-btn" lay-submit="" @click="loginAndRegister">注册/登录</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <footer-page></footer-page>
</template>

<script>
    export default {
        name: "Login",
        data() {
            return {
                activation: "login",
                msg: "",
                username: "",
                password: ""
            }
        },
        methods: {
            loginAndRegister: function () {
                this.axios.post('/api/v1/shopper/login/', {username: this.username, password: this.password}
                ).then(response => {
                    this.msg = response.data.msg
                    if (response.data.state === 'success') {
                        // 登录成功跳转个人主页
                        this.$store.commit('setUserName',this.username)
                        this.$store.commit('setLastLogin',response.data.last_login)
                        console.log(this.state)
                        this.$router.push({path: '/shopper'})
                    }
                })
                .catch(function (error) {
                    console.log(error)
                })
            }
        }
    }
</script>

<style scoped>

</style>
