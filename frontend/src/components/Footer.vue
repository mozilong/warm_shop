<template>
  <a-layout-footer class="footer">
    <div class="footer-content">
      <div class="footer-links">
        <div class="footer-column">
          <h3>关于我们</h3>
          <ul>
            <li><a href="#">公司简介</a></li>
            <li><a href="#">联系方式</a></li>
            <li><a href="#">招贤纳士</a></li>
          </ul>
        </div>
        <div class="footer-column">
          <h3>客户服务</h3>
          <ul>
            <li><a href="#">购物指南</a></li>
            <li><a href="#">售后服务</a></li>
            <li><a href="#">常见问题</a></li>
          </ul>
        </div>
        <div class="footer-column">
          <h3>支付方式</h3>
          <ul>
            <li><a href="#">支付宝</a></li>
            <li><a href="#">微信支付</a></li>
            <li><a href="#">银联支付</a></li>
          </ul>
        </div>
        <div class="footer-column">
          <h3>关注我们</h3>
          <div class="social-icons">
            <a-icon type="weibo-circle" class="icon" />
            <a-icon type="wechat" class="icon" />
            <a-icon type="github" class="icon" />
          </div>
          <p class="contact-phone">客服热线：400-123-4567</p>
        </div>
      </div>
      <div class="footer-copyright">
        <p>© 2025 暖心商城 All Rights Reserved. 版权所有</p>
      </div>
    </div>
  </a-layout-footer>
</template>

<script>
export default {
  name: 'Footer'
}
</script>

<style scoped>
.footer {
  background: #f8f8f8;
  padding: 40px 0 20px;
  margin-top: 40px;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.footer-links {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e8e8e8;
}

.footer-column {
  flex: 1;
  min-width: 200px;
  margin-bottom: 20px;
}

.footer-column h3 {
  font-size: 16px;
  margin-bottom: 15px;
  color: #333;
}

.footer-column ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-column li {
  margin-bottom: 8px;
}

.footer-column a {
  color: #666;
  text-decoration: none;
  font-size: 14px;
}

.footer-column a:hover {
  color: #1890ff;
}

.social-icons {
  display: flex;
  margin-bottom: 15px;
}

.icon {
  font-size: 24px;
  margin-right: 15px;
  color: #666;
  cursor: pointer;
}

.icon:hover {
  color: #1890ff;
}

.contact-phone {
  color: #666;
  font-size: 14px;
}

.footer-copyright {
  text-align: center;
  color: #999;
  font-size: 14px;
}
</style>