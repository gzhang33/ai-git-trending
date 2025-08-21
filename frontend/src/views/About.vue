<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
    <!-- 导航栏 -->
    <nav class="bg-slate-800/50 backdrop-blur-lg border-b border-slate-700">
      <div class="container mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <router-link to="/" class="text-white text-xl font-bold hover:text-blue-400 transition-colors">
            <i class="fas fa-rocket mr-2"></i>
            GitHub Trending Reporter
          </router-link>
          <router-link 
            to="/"
            class="bg-blue-500/20 text-blue-400 border border-blue-500/30 px-4 py-2 rounded-lg hover:bg-blue-500/30 transition-colors"
          >
            返回首页
          </router-link>
        </div>
      </div>
    </nav>

    <!-- 主要内容 -->
    <div class="container mx-auto px-6 py-12">
      <div class="max-w-4xl mx-auto">
        <!-- 项目介绍 -->
        <section class="bg-slate-800/50 backdrop-blur-lg rounded-2xl p-8 border border-slate-700 mb-8">
          <h1 class="text-3xl font-bold text-white mb-6 flex items-center">
            <i class="fas fa-info-circle mr-3 text-blue-400"></i>
            关于项目
          </h1>
          
          <div class="prose prose-invert max-w-none">
            <p class="text-slate-300 text-lg leading-relaxed mb-6">
              GitHub Trending Reporter 是一个自动化分析 GitHub Trending 的机器人，为您每日精选、总结并生成技术洞察报告。
            </p>
            
            <h3 class="text-white text-xl font-semibold mb-4">🌟 项目特色</h3>
            <ul class="text-slate-300 space-y-2">
              <li><strong>📈 智能分析</strong> - 利用大语言模型深度分析热门项目，生成技术洞察</li>
              <li><strong>🌐 现代界面</strong> - Vue 3 + TypeScript + Tailwind CSS 构建的响应式界面</li>
              <li><strong>🚀 实时数据</strong> - 每日自动抓取和分析最新的GitHub热门项目</li>
              <li><strong>📊 数据可视</strong> - 提供项目统计和趋势分析功能</li>
              <li><strong>💾 本地存储</strong> - 所有数据本地化存储，保护您的隐私</li>
            </ul>
          </div>
        </section>

        <!-- 技术栈 -->
        <section class="bg-slate-800/50 backdrop-blur-lg rounded-2xl p-8 border border-slate-700 mb-8">
          <h2 class="text-2xl font-bold text-white mb-6 flex items-center">
            <i class="fas fa-code mr-3 text-green-400"></i>
            技术栈
          </h2>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 class="text-lg font-semibold text-white mb-4">前端技术</h3>
              <div class="space-y-3">
                <div class="flex items-center">
                  <div class="w-4 h-4 bg-green-500 rounded mr-3"></div>
                  <span class="text-slate-300">Vue 3 + Composition API</span>
                </div>
                <div class="flex items-center">
                  <div class="w-4 h-4 bg-blue-500 rounded mr-3"></div>
                  <span class="text-slate-300">TypeScript</span>
                </div>
                <div class="flex items-center">
                  <div class="w-4 h-4 bg-cyan-500 rounded mr-3"></div>
                  <span class="text-slate-300">Tailwind CSS</span>
                </div>
                <div class="flex items-center">
                  <div class="w-4 h-4 bg-orange-500 rounded mr-3"></div>
                  <span class="text-slate-300">Vite</span>
                </div>
              </div>
            </div>
            
            <div>
              <h3 class="text-lg font-semibold text-white mb-4">后端技术</h3>
              <div class="space-y-3">
                <div class="flex items-center">
                  <div class="w-4 h-4 bg-yellow-500 rounded mr-3"></div>
                  <span class="text-slate-300">Python 3.x</span>
                </div>
                <div class="flex items-center">
                  <div class="w-4 h-4 bg-red-500 rounded mr-3"></div>
                  <span class="text-slate-300">Flask</span>
                </div>
                <div class="flex items-center">
                  <div class="w-4 h-4 bg-gray-500 rounded mr-3"></div>
                  <span class="text-slate-300">SQLite</span>
                </div>
                <div class="flex items-center">
                  <div class="w-4 h-4 bg-purple-500 rounded mr-3"></div>
                  <span class="text-slate-300">OpenAI API</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- 开源信息 -->
        <section class="bg-slate-800/50 backdrop-blur-lg rounded-2xl p-8 border border-slate-700">
          <h2 class="text-2xl font-bold text-white mb-6 flex items-center">
            <i class="fab fa-github mr-3 text-purple-400"></i>
            开源贡献
          </h2>
          
          <div class="text-center">
            <p class="text-slate-300 mb-6">
              这是一个开源项目，欢迎大家参与贡献！
            </p>
            
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
              <a 
                href="https://github.com/lgy1027/ai-git-trending" 
                target="_blank"
                class="bg-gray-800 text-white px-6 py-3 rounded-lg hover:bg-gray-700 transition-colors flex items-center justify-center"
              >
                <i class="fab fa-github mr-2"></i>
                查看源码
              </a>
              <a 
                href="https://github.com/lgy1027/ai-git-trending/issues" 
                target="_blank"
                class="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition-colors flex items-center justify-center"
              >
                <i class="fas fa-bug mr-2"></i>
                报告问题
              </a>
              <a 
                href="https://github.com/lgy1027/ai-git-trending/fork" 
                target="_blank"
                class="bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-600 transition-colors flex items-center justify-center"
              >
                <i class="fas fa-code-branch mr-2"></i>
                Fork 项目
              </a>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// About 页面逻辑
</script>