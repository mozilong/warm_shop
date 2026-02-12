<template>
  <div class="register-container">
    <h2>用户注册</h2>
    <form @submit.prevent="handleRegister" class="register-form">
      <div class="form-item">
        <label class="form-label">用户名</label>
        <input
          v-model="form.username"
          type="text"
          class="form-input"
          placeholder="请输入用户名（3-20位）"
        >
      </div>
      <div class="form-item">
        <label class="form-label">手机号</label>
        <input
          v-model="form.phone"
          type="tel"
          class="form-input"
          placeholder="请输入11位手机号（可选）"
        >
      </div>
      <div class="form-item">
        <label class="form-label">密码</label>
        <input
          v-model="form.password"
          type="password"
          class="form-input"
          placeholder="请输入6位以上密码"
        >
      </div>
      <div class="form-item">
        <label class="form-label">确认密码</label>
        <input
          v-model="form.confirmPwd"
          type="password"
          class="form-input"
          placeholder="请再次输入密码"
        >
      </div>
      <div class="tip-message" :class="{ success: tipType === 'success', error: tipType === 'error' }" v-if="tipMsg">
        {{ tipMsg }}
      </div>
      <button type="submit" class="register-btn" :disabled="loading">
        <span v-if="loading">注册中...</span>
        <span v-else>立即注册</span>
      </button>
    </form>
    <div class="login-link">
      已有账号？<a href="/login">立即登录</a>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const form = ref({
  username: '',
  phone: '',
  password: '',
  confirmPwd: ''
})

const tipMsg = ref('')
const tipType = ref('')
const loading = ref(false)

const handleRegister = async () => {
  tipMsg.value = ''
  tipType.value = ''

  if (!form.value.username.trim()) {
    tipMsg.value = '请输入用户名！'
    tipType.value = 'error'
    return
  }
  if (form.value.username.length < 3 || form.value.username.length > 20) {
    tipMsg.value = '用户名长度需在3-20位之间！'
    tipType.value = 'error'
    return
  }
  if (form.value.phone.trim() && !/^1[3-9]\d{9}$/.test(form.value.phone.trim())) {
    tipMsg.value = '请输入有效的11位手机号！'
    tipType.value = 'error'
    return
  }
  if (!form.value.password.trim()) {
    tipMsg.value = '请输入密码！'
    tipType.value = 'error'
    return
  }
  if (form.value.password.length < 6) {
    tipMsg.value = '密码长度不能少于6位！'
    tipType.value = 'error'
    return
  }
  if (form.value.password !== form.value.confirmPwd) {
    tipMsg.value = '两次输入的密码不一致！'
    tipType.value = 'error'
    return
  }

  loading.value = true
  try {
    // 仅执行注册，不自动登录
    const registerRes = await axios.post('/api/register/', {
      username: form.value.username.trim(),
      phone: form.value.phone.trim() || null,
      password: form.value.password.trim()
    })

    if (registerRes.data.code === 200) {
      tipMsg.value = '注册成功！即将跳转到登录页...'
      tipType.value = 'success'
      // 2秒后跳转到登录页
      setTimeout(() => {
        window.location.href = '/login'
      }, 2000)
    } else {
      tipMsg.value = registerRes.data.message
      tipType.value = 'error'
    }
  } catch (error) {
    console.error('注册异常：', error)
    tipMsg.value = '注册失败！请检查网络或稍后重试'
    tipType.value = 'error'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  max-width: 420px;
  margin: 50px auto;
  padding: 30px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(230, 67, 109, 0.1);
}

.register-container h2 {
  text-align: center;
  color: #e6436d;
  margin-bottom: 30px;
  font-size: 24px;
  font-weight: 600;
}

.register-form {
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

.register-btn {
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

.register-btn:hover {
  background-color: #d42858;
}

.register-btn:disabled {
  background-color: #ffb3c2;
  cursor: not-allowed;
}

.login-link {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: #666;
}

.login-link a {
  color: #e6436d;
  text-decoration: none;
  margin-left: 5px;
}

.login-link a:hover {
  color: #d42858;
  text-decoration: underline;
}
</style>
