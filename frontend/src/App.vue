<template>
  <el-container class="app-container">
    <el-header>
      <div class="header-content">
        <h1>OSINT 商情引擎</h1>
        <el-menu mode="horizontal" :router="true" :default-active="$route.path">
          <el-menu-item index="/">新建任务</el-menu-item>
          <el-menu-item index="/reports">历史报告</el-menu-item>
        </el-menu>
      </div>
    </el-header>
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
</script>

<style>
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
.app-container {
  min-height: 100vh;
}
.el-header {
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
  padding: 0 20px;
}
.header-content {
  display: flex;
  align-items: center;
  height: 60px;
  gap: 40px;
}
.header-content h1 {
  font-size: 18px;
  color: #303133;
  white-space: nowrap;
}
</style>
