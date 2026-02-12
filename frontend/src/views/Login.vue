<template>
  <div class="login-container">
    <h2>用户登录</h2>
    <form @submit.prevent="handleLogin" class="login-form">
      <div class="form-item">
        <label class="form-label">用户名</label>
        <input
          v-model="form.username"
          type="text"
          class="form-input"
          placeholder="请输入用户名"
        >
      </div>
      <div class="form-item">
        <label class="form-label">密码</label>
        <input
          v-model="form.password"
          type="password"
          class="form-input"
          placeholder="请输入密码"
        >
      </div>
      <div class="tip-message" :class="{ success: tipType === 'success', error: tipType === 'error' }" v-if="tipMsg">
        {{ tipMsg }}
      </div>
      <button type="submit" class="login-btn" :disabled="loading">
        <span v-if="loading">登录中...</span>
        <span v-else>立即登录</span>
      </button>
    </form>
    <div class="register-link">
      还没有账号？<a href="/register">立即注册</a>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const form = ref({
  username: '',
  password: ''
})

const tipMsg = ref('')
const tipType = ref('')
const loading = ref(false)

const handleLogin = async () => {
  tipMsg.value = ''
  tipType.value = ''

  if (!form.value.username.trim() || !form.value.password.trim()) {
    tipMsg.value = '用户名和密码不能为空！'
    tipType.value = 'error'
    return
  }

  loading.value = true
  try {
    // 登录请求（带斜杠，避免301重定向）
    const response = await axios.post('/api/login/', {
      username: form.value.username.trim(),
      password: form.value.password.trim()
    })

    if (response.data.code === 200) {
      localStorage.setItem('token', response.data.data.token)
      localStorage.setItem('userInfo', JSON.stringify(response.data.data.user))
      
      tipMsg.value = '登录成功！即将跳转到首页...'
      tipType.value = 'success'

      setTimeout(() => {
        window.location.href = '/'
      }, 2000)
    } else {
      tipMsg.value = response.data.message
      tipType.value = 'error'
    }
  } catch (error) {
    console.error('登录异常：', error)
    tipMsg.value = '登录失败！请检查网络或账号密码'
    tipType.value = 'error'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  max-width: 420px;
  margin: 50px auto;
  padding: 30px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(230, 67, 109, 0.1);
}

.login-container h2 {
  text-align: center;
  color: #e6436d;
  margin-bottom: 30px;
  font-size: 24px;
  font-weight: 600;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-label {
  font-size: 14px;
  color: #e6436d;
  font-weight: 500;
}

.form-input {
  padding: 12px 15px;
  border: 1px solid #ff8ca8;
  border-radius: 4px;
  font-size: 14px;
  color: #333;
}

.form-input:focus {
  outline: none;
  border-color: #e6436d;
  box-shadow: 0 0 6px rgba(230, 67, 109, 0.2);
}

.tip-message {
  padding: 10px;
  border-radius: 4px;
  font-size: 13px;
  text-align: center;
  margin-top: 5px;
}

.tip-message.success {
  background-color: #f0fff4;
  color: #00b42a;
  border: 1px solid #b7eb8f;
}

.tip-message.error {
  background-color: #fff2f0;
  color: #f5222d;
  border: 1px solid #ffccc7;
}

.login-btn {
  padding: 14px;
  background-color: #e6436d;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-top: 10px;
}

.login-btn:hover {
  background-color: #d42858;
}

.login-btn:disabled {
  background-color: #ffb3c2;
  cursor: not-allowed;
}

.register-link {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: #666;
}

.register-link a {
  color: #e6436d;
  text-decoration: none;
  margin-left: 5px;
}

.register-link a:hover {
  color: #d42858;
  text-decoration: underline;
}
</style>
