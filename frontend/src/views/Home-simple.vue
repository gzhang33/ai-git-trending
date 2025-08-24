<template>
  <div class="bg-gradient-to-br from-slate-800 to-slate-900 text-slate-100 min-h-screen font-sans theme-transition">
    <!-- 顶部菜单栏 -->
    <header class="fixed top-0 right-0 z-50 p-4">
      <div class="flex items-center space-x-4">
        <!-- 技术趋势分析按钮 -->
        <button
          @click="() => { showTrendsModal = true; loadTrendsData(); }"
          class="glass-card px-4 py-2 rounded-lg text-slate-300 hover:text-white transition-all duration-200 hover:scale-105 border border-white/10 hover:border-blue-400/50 backdrop-blur-sm flex items-center space-x-2"
        >
          <i class="fa fa-bar-chart"></i>
          <span class="hidden sm:inline">技术趋势分析</span>
        </button>
        
        <!-- 联系我们按钮 -->
        <div class="relative group">
          <button
            class="glass-card px-4 py-2 rounded-lg text-slate-300 hover:text-white transition-all duration-200 hover:scale-105 border border-white/10 hover:border-green-400/50 backdrop-blur-sm flex items-center space-x-2"
          >
            <!-- 微信图标 SVG -->
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
              <path d="M8.691 2.188C3.891 2.188 0 5.476 0 9.53c0 2.212 1.172 4.203 3.002 5.55a.59.59 0 0 1 .213.665l-.39 1.48c-.019.07-.048.141-.048.213 0 .163.13.295.29.295a.326.326 0 0 0 .167-.054l1.903-1.114a.864.864 0 0 1 .717-.098 10.16 10.16 0 0 0 2.837.403c.276 0 .543-.027.811-.05-.857-2.578.157-4.972 1.932-6.446 1.703-1.415 4.882-1.157 6.654.701.442-3.243-2.666-6.077-8.426-6.077zm-3.26 8.067c-.315 0-.572-.261-.572-.583 0-.322.257-.583.572-.583.316 0 .572.261.572.583 0 .322-.256.583-.572.583zm6.527 0c-.315 0-.572-.261-.572-.583 0-.322.257-.583.572-.583.316 0 .572.261.572.583 0 .322-.256.583-.572.583z"/>
              <path d="M15.977 9.901c-3.839 0-6.943 2.61-6.943 5.831 0 1.925 1.5 3.652 3.839 4.835-.315-1.186-.315-2.372 0-3.558-.315 0-.63-.157-.63-.471 0-.315.315-.473.63-.473s.63.158.63.473c0 .314-.315.471-.63.471 1.5 1.5 3.839 1.5 5.339 0-.315 0-.63-.157-.63-.471 0-.315.315-.473.63-.473s.63.158.63.473c0 .314-.315.471-.63.471 1.185 1.186 1.185 3.558 0 4.835 2.339-1.183 3.839-2.91 3.839-4.835 0-3.221-3.104-5.831-6.943-5.831z"/>
            </svg>
            <span class="hidden sm:inline">联系我们</span>
          </button>
          
          <!-- 悬停显示的微信二维码 -->
          <div class="absolute hidden group-hover:block right-0 top-full mt-2 z-50">
            <div class="bg-white p-3 rounded-lg shadow-2xl border border-slate-200 wechat-qr-card">
              <img :src="wechatImageUrl" alt="微信公众号二维码" class="w-32 h-32 mx-auto block">
              <p class="text-center text-xs text-slate-600 mt-2 font-medium whitespace-nowrap">扫码关注微信公众号</p>
            </div>
            <!-- 小三角箭头 -->
            <div class="absolute top-0 right-4 transform -translate-y-1/2 rotate-45 w-2 h-2 bg-white border-l border-t border-slate-200"></div>
          </div>
        </div>
        
        <!-- 主题切换按钮（放在最右侧） -->
        <div class="relative group theme-switcher">
          <button
            @click="toggleTheme"
            class="glass-card px-4 py-2 rounded-lg text-slate-300 hover:text-white transition-all duration-200 hover:scale-105 border border-white/10 hover:border-yellow-400/50 backdrop-blur-sm flex items-center space-x-2"
          >
            <!-- 主题图标 -->
            <svg v-if="currentTheme === 'dark'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path>
            </svg>
            <svg v-else-if="currentTheme === 'light'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path>
            </svg>
            <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
            </svg>
            <span class="hidden sm:inline text-sm font-medium">{{ getThemeLabel() }}</span>
          </button>
          
          <!-- 主题选择下拉菜单 -->
          <div v-if="showThemeMenu" class="absolute right-0 top-full mt-2 z-50 bg-slate-800/90 backdrop-blur-xl rounded-xl border border-slate-600/50 shadow-2xl min-w-[150px] overflow-hidden">
            <div 
              v-for="theme in themes" 
              :key="theme.value"
              @click="setTheme(theme.value)"
              class="px-4 py-3 hover:bg-slate-700/50 cursor-pointer transition-colors flex items-center space-x-3 text-sm"
              :class="{ 'bg-slate-700/30': currentTheme === theme.value }"
            >
              <component :is="theme.icon" class="w-4 h-4" />
              <span class="text-slate-200">{{ theme.label }}</span>
              <svg v-if="currentTheme === theme.value" class="w-3 h-3 ml-auto text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </header>
    <!-- 粒子背景效果 -->
    <div class="fixed inset-0 -z-10 overflow-hidden">
      <div class="absolute top-[10%] left-[20%] w-64 h-64 bg-blue-500/20 rounded-full filter blur-3xl animate-pulse-slow"></div>
      <div class="absolute top-[60%] right-[15%] w-80 h-80 bg-purple-500/20 rounded-full filter blur-3xl animate-pulse-slow delay-1000"></div>
      <div class="absolute bottom-[10%] left-[30%] w-72 h-72 bg-pink-500/20 rounded-full filter blur-3xl animate-pulse-slow delay-2000"></div>
    </div>

    <!-- 主内容区 -->
    <div class="container mx-auto px-4 py-12">
      <h1 class="text-4xl font-bold text-center mb-8">
        <span style="background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899); background-clip: text; -webkit-background-clip: text; color: transparent;">
          GitHub每周热门项目
        </span>
      </h1>
      
      <div class="text-center mb-8">
        <p class="text-slate-400 text-lg mb-6">探索 GitHub 每日热门开源项目，点击日期卡片查看详细分析报告</p>
        
        <!-- 快速导航栏 -->
        <div class="flex flex-wrap justify-center items-center gap-4 mb-8">
          <div class="glass-card rounded-full px-6 py-3 border border-slate-600/50 hover:border-blue-400/50 transition-all duration-200">
            <div class="flex items-center space-x-3">
              <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
              <input 
                v-model="searchQuery" 
                @input="filterReports"
                type="text" 
                placeholder="搜索报告..." 
                class="bg-transparent text-slate-300 placeholder-slate-500 outline-none w-32 sm:w-48"
              >
            </div>
          </div>
          
          <select 
            v-model="selectedTimeRange" 
            @change="filterReports"
            class="glass-card rounded-full px-4 py-3 border border-slate-600/50 hover:border-purple-400/50 transition-all duration-200 bg-transparent text-slate-300 outline-none cursor-pointer"
          >
            <option value="all">全部时间</option>
            <option value="week">本周</option>
            <option value="month">本月</option>
            <option value="quarter">本季度</option>
          </select>
          
          <div class="glass-card rounded-full px-4 py-3 border border-slate-600/50 hover:border-green-400/50 transition-all duration-200 cursor-pointer" @click="refreshAll">
            <div class="flex items-center space-x-2">
              <svg class="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
              </svg>
              <span class="text-sm font-medium text-green-400">刷新</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 项目概览仪表板 -->
      <div v-if="!loading && !error" class="mb-12">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <!-- 总报告数 -->
          <div class="glass-card rounded-2xl p-6 border border-slate-600/50 hover:border-blue-400/50 transition-all duration-200">
            <div class="flex items-center justify-between mb-4">
              <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
              </div>
              <div class="text-right">
                <div class="text-2xl font-bold text-white">{{ animatedStats.totalReports }}</div>
                <div class="text-xs text-slate-400">总报告数</div>
              </div>
            </div>
            <div class="text-xs text-green-400 flex items-center">
              <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
              </svg>
              持续增长
            </div>
          </div>
          
          <!-- 总项目数 -->
          <div class="glass-card rounded-2xl p-6 border border-slate-600/50 hover:border-purple-400/50 transition-all duration-200">
            <div class="flex items-center justify-between mb-4">
              <div class="w-12 h-12 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl flex items-center justify-center">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                </svg>
              </div>
              <div class="text-right">
                <div class="text-2xl font-bold text-white">{{ animatedStats.totalProjects }}</div>
                <div class="text-xs text-slate-400">总项目数</div>
              </div>
            </div>
            <div class="text-xs text-blue-400 flex items-center">
              <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
              </svg>
              发现新项目
            </div>
          </div>
          
          <!-- 热门语言 -->
          <div class="glass-card rounded-2xl p-6 border border-slate-600/50 hover:border-pink-400/50 transition-all duration-200">
            <div class="flex items-center justify-between mb-4">
              <div class="w-12 h-12 bg-gradient-to-br from-pink-500 to-pink-600 rounded-xl flex items-center justify-center">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
                </svg>
              </div>
              <div class="text-right">
                <div class="text-xl font-bold text-white">{{ stats.topLanguage || 'Loading...' }}</div>
                <div class="text-xs text-slate-400">热门语言</div>
              </div>
            </div>
            <div class="text-xs text-pink-400 flex items-center">
              <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z"></path>
              </svg>
              本周最热
            </div>
          </div>
          
          <!-- 本周新增 -->
          <div class="glass-card rounded-2xl p-6 border border-slate-600/50 hover:border-green-400/50 transition-all duration-200">
            <div class="flex items-center justify-between mb-4">
              <div class="w-12 h-12 bg-gradient-to-br from-green-500 to-green-600 rounded-xl flex items-center justify-center">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                </svg>
              </div>
              <div class="text-right">
                <div class="text-2xl font-bold text-white">{{ animatedStats.weeklyNew }}</div>
                <div class="text-xs text-slate-400">本周新增</div>
              </div>
            </div>
            <div class="text-xs text-green-400 flex items-center">
              <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              实时更新
            </div>
          </div>
        </div>
        
        <!-- 最近热门项目预览 -->
        <div v-if="recentHotProjects.length > 0" class="glass-card rounded-2xl p-6 border border-slate-600/50 mb-8">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-xl font-bold text-white flex items-center">
              <svg class="w-5 h-5 mr-2 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
              </svg>
              最近热门项目
            </h3>
            <button 
              @click="() => { showTrendsModal = true; loadTrendsData(); }"
              class="text-blue-400 hover:text-blue-300 transition-colors text-sm flex items-center"
            >
              查看更多
              <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
              </svg>
            </button>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div 
              v-for="(project, index) in recentHotProjects.slice(0, 6)" 
              :key="index" 
              class="bg-slate-700/30 rounded-xl p-4 border border-slate-600/30 hover:border-blue-400/50 transition-all duration-200"
            >
              <div class="flex items-start justify-between mb-2">
                <h4 class="font-medium text-white text-sm truncate flex-1">{{ project.name }}</h4>
                <div class="flex items-center space-x-1 text-yellow-400 text-xs ml-2">
                  <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                  </svg>
                  <span>{{ (project.avg_stars || project.stars || 0).toLocaleString() }}</span>
                </div>
              </div>
              <p class="text-slate-400 text-xs mb-3 line-clamp-2">{{ project.description || '暂无描述' }}</p>
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-1">
                  <div class="w-2 h-2 rounded-full" :class="getLanguageColor(project.language)"></div>
                  <span class="text-slate-400 text-xs">{{ project.language || 'Unknown' }}</span>
                </div>
                <span class="text-blue-400 text-xs">上榜 {{ project.count || 1 }} 次</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 显示加载状态 -->
      <div v-if="loading" class="text-center py-16">
        <div class="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
        <p class="text-slate-400">加载报告中...</p>
      </div>
      
      <!-- 显示错误 -->
      <div v-else-if="error" class="text-center py-20">
        <div class="max-w-md mx-auto glass-card rounded-2xl p-8">
          <div class="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg class="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-red-400 mb-4">加载失败</h3>
          <p class="text-slate-400 mb-6">{{ error }}</p>
          <button @click="fetchReports" class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg transition-colors">
            重试
          </button>
        </div>
      </div>
      
      <!-- 显示报告列表 -->
      <div v-else-if="filteredReports.length > 0 || reports.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <div 
          v-for="(report, index) in (filteredReports.length > 0 || searchQuery || selectedTimeRange !== 'all' ? filteredReports : reports)" 
          :key="report.date"
          class="report-card bg-gradient-to-br from-slate-800/60 to-slate-900/60 rounded-3xl overflow-hidden border border-white/10 hover:border-white/20 cursor-pointer backdrop-blur-xl group transition-all duration-500 hover:transform hover:scale-105 hover:shadow-2xl"
          :style="{ animationDelay: `${index * 0.1}s` }"
          @click="() => openReport(report.date)"
        >
          <!-- 背景装饰 -->
          <div class="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          
          <!-- 最新标识 -->
          <div v-if="index === 0" class="absolute top-4 right-4 z-10">
            <div class="bg-gradient-to-r from-pink-500 to-rose-500 text-white text-xs px-3 py-1 rounded-full shadow-lg">
              <i class="fa fa-star mr-1"></i>最新
            </div>
          </div>
          
          <!-- 卡片内容 -->
          <div class="relative p-6">
            <!-- 日期大标题 -->
            <div class="mb-6">
              <div class="text-slate-400 text-sm font-medium mb-2 flex items-center">
                <i class="fa fa-calendar mr-2 text-blue-400"></i>
                {{ formatDateShort(report.date) }}
              </div>
              <div class="relative">
                <div class="text-6xl font-black text-transparent bg-gradient-to-br from-blue-400 via-purple-400 to-pink-400 bg-clip-text">
                  {{ formatDay(report.date) }}
                </div>
                <div class="absolute -bottom-1 left-0 w-12 h-1 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full opacity-60"></div>
              </div>
              <div class="text-slate-300 text-sm mt-2 font-medium">
                {{ formatDateWeek(report.date) }}
              </div>
            </div>
            
            <!-- 项目统计 -->
            <div class="mb-6">
              <div class="flex items-center justify-between bg-slate-700/30 rounded-xl p-3 border border-slate-600/30">
                <div class="flex items-center">
                  <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-500 rounded-lg flex items-center justify-center mr-3">
                    <i class="fa fa-cube text-white text-sm"></i>
                  </div>
                  <div>
                    <div class="text-slate-300 text-sm">项目数量</div>
                    <div class="text-lg font-bold text-white">{{ report.project_count }}</div>
                  </div>
                </div>
                <div class="text-right">
                  <div class="text-slate-400 text-xs">点击查看</div>
                  <div class="text-blue-400 text-lg">
                    <i class="fa fa-arrow-right"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 底部装饰线 -->
          <div class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 opacity-60 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>
      </div>
      
      <!-- 空数据状态 -->
      <div v-else class="text-center py-20">
        <div class="max-w-md mx-auto">
          <div class="w-24 h-24 bg-slate-700/50 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg class="w-12 h-12 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-slate-300 mb-4">暂无报告</h3>
          <p class="text-slate-400 mb-6">还没有生成任何报告</p>
          <button @click="fetchReports" class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg transition-colors">
            刷新数据
          </button>
        </div>
      </div>
    </div>
    
    <!-- 技术趋势分析模态框 -->
    <div v-if="showTrendsModal" class="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4" @click="closeTrendsModal">
      <div class="bg-slate-800 rounded-2xl max-w-6xl w-full max-h-[90vh] overflow-hidden" @click.stop>
        <!-- 模态框头部 -->
        <div class="flex items-center justify-between p-6 border-b border-slate-600">
          <h3 class="text-xl font-bold text-white">技术趋势分析</h3>
          <button @click="closeTrendsModal" class="text-slate-400 hover:text-white transition-colors">
            <i class="fa fa-times text-xl"></i>
          </button>
        </div>
        
        <!-- 模态框内容 -->
        <div class="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
          <div v-if="trendsLoading" class="text-center py-16">
            <div class="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p class="text-slate-400">加载趋势数据中...</p>
          </div>
          
          <div v-else-if="trendsError" class="text-center py-12">
            <div class="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01"></path>
              </svg>
            </div>
            <div class="text-red-400 mb-4">{{ trendsError }}</div>
            <button @click="loadTrendsData" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded transition-colors">
              重试
            </button>
          </div>
          
          <div v-else-if="trendsData" class="space-y-8">
            <!-- 趋势数据展示 -->
            <div class="text-center mb-8">
              <h2 class="text-2xl font-bold mb-4">技术趋势洞察</h2>
              <p class="text-slate-400 max-w-2xl mx-auto">基于历史数据分析 GitHub 的技术热点、窜升项目和语言趋势。</p>
            </div>
            
            <!-- 热门项目和语言 -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div class="bg-slate-700/50 p-6 rounded-2xl border border-slate-600">
                <h3 class="text-xl font-bold mb-4">热门项目 (近7天)</h3>
                <div v-if="trendsData.most_frequent_projects?.length > 0" class="space-y-4">
                  <div v-for="(project, index) in trendsData.most_frequent_projects.slice(0, 6)" :key="index" 
                       class="bg-slate-800/50 p-4 rounded-xl border border-slate-600/50 hover:border-blue-400/50 transition-all duration-200 hover:transform hover:scale-[1.02] group">
                    <!-- 项目头部信息 -->
                    <div class="flex items-start justify-between mb-3">
                      <div class="flex-1">
                        <a :href="project.url" target="_blank" rel="noopener noreferrer" 
                           class="font-semibold text-blue-300 hover:text-blue-200 transition-colors flex items-center space-x-2 mb-1">
                          <span class="text-lg">{{ project.name }}</span>
                          <svg class="w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity" 
                               fill="currentColor" viewBox="0 0 20 20">
                            <path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z"></path>
                            <path d="M5 5a2 2 0 00-2 2v6a2 2 0 002 2h6a2 2 0 002-2v-2a1 1 0 10-2 0v2H5V7h2a1 1 0 000-2H5z"></path>
                          </svg>
                        </a>
                        <p class="text-slate-400 text-sm leading-relaxed">{{ project.description || '暂无描述' }}</p>
                      </div>
                    </div>
                    
                    <!-- 项目统计信息 -->
                    <div class="flex items-center justify-between">
                      <div class="flex items-center space-x-4">
                        <div class="flex items-center space-x-1">
                          <div class="w-3 h-3 rounded-full" :class="getLanguageColor(project.language)"></div>
                          <span class="text-slate-300 text-sm font-medium">{{ project.language }}</span>
                        </div>
                        <div class="flex items-center space-x-1 text-yellow-400">
                          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                          </svg>
                          <span class="text-sm font-medium">{{ project.avg_stars.toLocaleString() }}</span>
                        </div>
                      </div>
                      <div class="bg-blue-500/20 text-blue-300 px-3 py-1 rounded-full text-sm font-medium">
                        上榜 {{ project.count }} 次
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else class="text-slate-400 text-center py-8">暂无数据</div>
              </div>
              
              <div class="bg-slate-700/50 p-6 rounded-2xl border border-slate-600">
                <h3 class="text-xl font-bold mb-4">热门语言 (近7天)</h3>
                <div v-if="trendsData.most_frequent_languages?.length > 0" class="space-y-3">
                  <div v-for="(language, index) in trendsData.most_frequent_languages.slice(0, 8)" :key="index" 
                       class="flex items-center justify-between bg-slate-800/50 p-3 rounded-lg">
                    <span class="font-medium text-pink-300">{{ language[0] }}</span>
                    <span class="text-slate-400">上榜 {{ language[1] }} 次</span>
                  </div>
                </div>
                <div v-else class="text-slate-400 text-center py-8">暂无数据</div>
              </div>
            </div>
            
            <!-- 窜升项目 -->
            <div class="bg-slate-700/50 p-6 rounded-2xl border border-slate-600">
              <h3 class="text-xl font-bold mb-4">星标窜升最快项目 (近7天)</h3>
              <div v-if="trendsData.surging_projects?.length > 0" class="space-y-4">
                <div v-for="(project, index) in trendsData.surging_projects" :key="index" 
                     class="bg-slate-800/50 p-4 rounded-xl border border-slate-600/50 hover:border-green-400/50 transition-all duration-200 hover:transform hover:scale-[1.02] group">
                  <!-- 项目头部 -->
                  <div class="flex items-start justify-between mb-3">
                    <a :href="project.url" target="_blank" rel="noopener noreferrer" 
                       class="font-medium text-purple-300 hover:text-purple-200 transition-colors flex items-center space-x-2 group-hover:text-purple-100">
                      <span class="text-lg">{{ project.name }}</span>
                      <svg class="w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity" 
                           fill="currentColor" viewBox="0 0 20 20">
                        <path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z"></path>
                        <path d="M5 5a2 2 0 00-2 2v6a2 2 0 002 2h6a2 2 0 002-2v-2a1 1 0 10-2 0v2H5V7h2a1 1 0 000-2H5z"></path>
                      </svg>
                    </a>
                    <div class="bg-green-500/20 text-green-300 px-3 py-1 rounded-full text-sm font-bold flex items-center space-x-1">
                      <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"></path>
                      </svg>
                      <span>+{{ project.star_increase.toLocaleString() }}</span>
                    </div>
                  </div>
                  
                  <!-- 项目描述 -->
                  <p v-if="project.description" class="text-slate-400 text-sm mb-3 leading-relaxed">
                    {{ project.description }}
                  </p>
                  
                  <!-- 项目统计信息 -->
                  <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-4">
                      <!-- 编程语言 -->
                      <div class="flex items-center space-x-1">
                        <div class="w-3 h-3 rounded-full" :class="getLanguageColor(project.language)"></div>
                        <span class="text-slate-300 text-sm font-medium">{{ project.language }}</span>
                      </div>
                      
                      <!-- 星标变化详情 -->
                      <div class="flex items-center space-x-2 text-xs text-slate-400">
                        <div class="flex items-center space-x-1">
                          <span>{{ project.start_stars.toLocaleString() }}</span>
                          <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"></path>
                          </svg>
                          <span class="text-green-400 font-medium">{{ project.end_stars.toLocaleString() }}</span>
                        </div>
                      </div>
                    </div>
                    
                    <!-- 增长百分比 -->
                    <div class="text-right">
                      <div class="text-green-400 font-bold text-sm">
                        +{{ Math.round((project.star_increase / project.start_stars) * 100) }}%
                      </div>
                      <div class="text-xs text-slate-500">7天增长</div>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="text-slate-400 text-center py-8">暂无星标数明显窜升的项目</div>
            </div>
          </div>
          
          <div v-else class="text-center py-16">
            <div class="text-slate-400 mb-4">点击下方按钮加载趋势数据</div>
            <button @click="loadTrendsData" class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg transition-colors">
              加载趋势数据
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 报告详情模态框 -->
    <div v-if="showModal" class="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4" @click="closeModal">
      <div class="bg-slate-800 rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden" @click.stop>
        <!-- 模态框头部 -->
        <div class="flex items-center justify-between p-6 border-b border-slate-600">
          <h3 class="text-xl font-bold text-white">报告详情 - {{ currentReport?.date }}</h3>
          <button @click="closeModal" class="text-slate-400 hover:text-white transition-colors">
            <i class="fa fa-times text-xl"></i>
          </button>
        </div>
        
        <!-- 模态框内容 -->
        <div class="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
          <div v-if="loadingContent" class="text-center py-12">
            <div class="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p class="text-slate-400">加载报告内容中...</p>
          </div>
          
          <div v-else-if="reportError" class="text-center py-12">
            <div class="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01"></path>
              </svg>
            </div>
            <div class="text-red-400 mb-4">{{ reportError }}</div>
            <button @click="loadReportContent(currentReport?.date)" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded transition-colors">
              重试
            </button>
          </div>
          
          <div v-else-if="renderedContent" class="markdown-content prose prose-invert max-w-none" v-html="renderedContent"></div>
          
          <div v-else class="text-center py-12">
            <div class="text-slate-400">暂无内容</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, computed, onUnmounted } from 'vue'
import { getReports, reportApi, type Report } from '../api/reports'
import { renderMarkdown, enhanceMarkdownDisplay } from '../utils/markdown-simple'

// 响应式数据
const reports = ref<Report[]>([])
const filteredReports = ref<Report[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const showModal = ref(false)
const currentReport = ref<Report | null>(null)
const reportContent = ref<string | null>(null)
const renderedContent = ref<string | null>(null)
const loadingContent = ref(false)
const reportError = ref<string | null>(null)
const API_BASE_URL = 'http://localhost:5001'
const wechatImageUrl = `${API_BASE_URL}/images/wechat.png`

// 新增功能相关数据
const searchQuery = ref('')
const selectedTimeRange = ref('all')
const stats = ref<any>({})
const animatedStats = ref({
  totalReports: 0,
  totalProjects: 0,
  weeklyNew: 0
})
const recentHotProjects = ref<any[]>([])

// 菜单相关状态
const showTrendsModal = ref(false)
const trendsData = ref<any>(null)
const trendsLoading = ref(false)
const trendsError = ref<string | null>(null)

// 主题相关状态
const currentTheme = ref<string>('dark')
const showThemeMenu = ref(false)
const themes = ref([
  {
    value: 'dark',
    label: '深色主题',
    icon: 'svg'
  },
  {
    value: 'light', 
    label: '浅色主题',
    icon: 'svg'
  },
  {
    value: 'test',
    label: '测试主题',
    icon: 'svg'
  },
  {
    value: 'auto',
    label: '跟随系统',
    icon: 'svg'
  },
  {
    value: 'blue',
    label: '深蓝主题',
    icon: 'svg'
  },
  {
    value: 'purple',
    label: '紫色主题',
    icon: 'svg'
  }
])

// 获取报告列表
async function fetchReports() {
  try {
    loading.value = true
    error.value = null
    console.log('📊 开始获取报告列表...')
    
    // 并行获取报告列表和统计数据
    const [reportsData, statsData] = await Promise.all([
      getReports(),
      fetchStats()
    ])
    
    reports.value = reportsData || []
    filteredReports.value = reports.value
    
    // 启动数字动画
    animateNumbers(statsData)
    
    // 获取热门项目预览
    await fetchRecentHotProjects()
    
    console.log('✅ 报告获取成功:', reports.value.length, '个报告')
  } catch (err: any) {
    error.value = err.message || '获取报告列表失败'
    console.error('❌ 获取报告失败:', err)
  } finally {
    loading.value = false
  }
}

// 获取统计数据
async function fetchStats() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/stats`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    stats.value = data
    return data
  } catch (err) {
    console.error('❌ 获取统计数据失败:', err)
    return {
      totalReports: reports.value.length,
      totalProjects: 0,
      topLanguage: 'N/A',
      weeklyNew: 0
    }
  }
}

// 数字动画
function animateNumbers(targetStats: any) {
  const duration = 1500
  const steps = 60
  const interval = duration / steps
  
  let currentStep = 0
  const timer = setInterval(() => {
    const progress = currentStep / steps
    const easeProgress = 1 - Math.pow(1 - progress, 3) // 缓出动画
    
    animatedStats.value.totalReports = Math.floor((targetStats.totalReports || 0) * easeProgress)
    animatedStats.value.totalProjects = Math.floor((targetStats.totalProjects || 0) * easeProgress)
    animatedStats.value.weeklyNew = Math.floor((targetStats.weeklyNew || 0) * easeProgress)
    
    currentStep++
    if (currentStep > steps) {
      clearInterval(timer)
      // 确保最终值的准确性
      animatedStats.value.totalReports = targetStats.totalReports || 0
      animatedStats.value.totalProjects = targetStats.totalProjects || 0
      animatedStats.value.weeklyNew = targetStats.weeklyNew || 0
    }
  }, interval)
}

// 获取最近热门项目
async function fetchRecentHotProjects() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/trends`)
    if (response.ok) {
      const data = await response.json()
      recentHotProjects.value = data.most_frequent_projects || []
    }
  } catch (err) {
    console.error('❌ 获取热门项目失败:', err)
  }
}

// 筛选报告
function filterReports() {
  let filtered = [...reports.value]
  
  // 按搜索关键词筛选
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim()
    filtered = filtered.filter(report => 
      report.date.toLowerCase().includes(query) ||
      formatDateShort(report.date).toLowerCase().includes(query)
    )
  }
  
  // 按时间范围筛选
  if (selectedTimeRange.value !== 'all') {
    const now = new Date()
    const cutoffDate = new Date()
    
    switch (selectedTimeRange.value) {
      case 'week':
        cutoffDate.setDate(now.getDate() - 7)
        break
      case 'month':
        cutoffDate.setMonth(now.getMonth() - 1)
        break
      case 'quarter':
        cutoffDate.setMonth(now.getMonth() - 3)
        break
    }
    
    filtered = filtered.filter(report => {
      const reportDate = new Date(report.date)
      return reportDate >= cutoffDate
    })
  }
  
  filteredReports.value = filtered
}

// 刷新所有数据
async function refreshAll() {
  searchQuery.value = ''
  selectedTimeRange.value = 'all'
  await fetchReports()
}

// 加载报告内容
async function loadReportContent(date?: string) {
  if (!date) return
  
  try {
    loadingContent.value = true
    reportError.value = null
    console.log('📄 加载报告内容:', date)
    const report = await reportApi.getReportContent(date)
    reportContent.value = report.content || '暂无内容'
    
    // 渲染Markdown内容
    if (reportContent.value) {
      console.log('🎨 渲染Markdown内容...')
      renderedContent.value = renderMarkdown(reportContent.value)
      
      // 在下一个tick中增强显示效果
      await nextTick()
      const modalContent = document.querySelector('.markdown-content')
      if (modalContent) {
        console.log('✨ 增强显示效果...')
        enhanceMarkdownDisplay(modalContent as HTMLElement)
      }
    }
    
    console.log('✅ 报告内容加载成功')
  } catch (err: any) {
    reportError.value = err.message || '加载报告内容失败'
    console.error('❌ 加载报告内容失败:', err)
  } finally {
    loadingContent.value = false
  }
}

// 打开报告
async function openReport(date: string) {
  console.log('🎯 点击报告卡片:', date)
  const report = reports.value.find(r => r.date === date)
  if (report) {
    currentReport.value = report
    showModal.value = true
    console.log('📂 打开模态框，加载内容...')
    await loadReportContent(date)
  } else {
    console.error('❌ 未找到报告:', date)
  }
}

// 关闭模态框
function closeModal() {
  console.log('📋 关闭模态框')
  showModal.value = false
  currentReport.value = null
  reportContent.value = null
  renderedContent.value = null
  reportError.value = null
  loadingContent.value = false
}

// 日期格式化函数
function formatDateShort(dateStr: string): string {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    month: 'short',
    day: 'numeric',
    weekday: 'short'
  })
}

function formatDay(dateStr: string): string {
  const date = new Date(dateStr)
  return date.getDate().toString()
}

function formatDateWeek(dateStr: string): string {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    weekday: 'long'
  })
}

// 组件挂载时获取数据
onMounted(async () => {
  console.log('🚀 组件挂载，开始初始化...')
  
  // 初始化主题
  initTheme()
  
  // 添加点击外部事件监听
  document.addEventListener('click', handleClickOutside)
  
  // 监听系统主题变化（对于自动主题）
  if (window.matchMedia) {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    mediaQuery.addListener(() => {
      if (currentTheme.value === 'auto') {
        applyTheme('auto')
      }
    })
  }
  
  await fetchReports()
})

// 组件卸载时清理事件监听
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

// 加载趋势数据
async function loadTrendsData() {
  try {
    trendsLoading.value = true
    trendsError.value = null
    console.log('📈 开始获取趋势数据...')
    
    const response = await fetch(`${API_BASE_URL}/api/trends`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    trendsData.value = data
    console.log('✅ 趋势数据获取成功:', data)
  } catch (err: any) {
    trendsError.value = err.message || '获取趋势数据失败'
    console.error('❌ 获取趋势数据失败:', err)
  } finally {
    trendsLoading.value = false
  }
}

// 关闭趋势模态框
function closeTrendsModal() {
  showTrendsModal.value = false
  trendsData.value = null
  trendsError.value = null
}

// 获取编程语言颜色
function getLanguageColor(language: string): string {
  const colors: Record<string, string> = {
    'TypeScript': 'bg-blue-500',
    'JavaScript': 'bg-yellow-500', 
    'Python': 'bg-green-500',
    'Java': 'bg-orange-500',
    'C++': 'bg-purple-500',
    'C': 'bg-gray-500',
    'Rust': 'bg-red-500',
    'Go': 'bg-cyan-500',
    'Vue': 'bg-emerald-500',
    'React': 'bg-sky-500',
    'PHP': 'bg-indigo-500',
    'Ruby': 'bg-red-400',
    'Swift': 'bg-orange-400',
    'Kotlin': 'bg-purple-400',
    'Dart': 'bg-blue-400',
    'Zig': 'bg-amber-500'
  }
  return colors[language] || 'bg-slate-500'
}

// 主题相关方法
function initTheme() {
  // 从 localStorage 读取保存的主题
  const savedTheme = localStorage.getItem('theme') || 'dark'
  console.log('📂 初始化主题:', savedTheme)
  currentTheme.value = savedTheme
  applyTheme(savedTheme)
}

function toggleTheme() {
  showThemeMenu.value = !showThemeMenu.value
}

function setTheme(theme: string) {
  console.log('🎨 切换主题到:', theme)
  currentTheme.value = theme
  localStorage.setItem('theme', theme)
  applyTheme(theme)
  showThemeMenu.value = false
  
  // 显示主题切换提示
  const themeLabels: Record<string, string> = {
    'dark': '深色主题',
    'light': '浅色主题', 
    'auto': '跟随系统',
    'blue': '深蓝主题',
    'purple': '紫色主题'
  }
  console.log('✨ 已切换到:', themeLabels[theme])
}

function applyTheme(theme: string) {
  const body = document.body
  const html = document.documentElement
  
  // 移除所有主题类
  const themeClasses = ['theme-dark', 'theme-light', 'theme-auto', 'theme-blue', 'theme-purple', 'theme-test']
  themeClasses.forEach(cls => {
    body.classList.remove(cls)
    html.classList.remove(cls)
  })
  
  console.log('📦 移除旧主题类，添加新主题:', theme)
  
  // 添加新主题类
  if (theme === 'auto') {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    const actualTheme = prefersDark ? 'theme-dark' : 'theme-light'
    body.classList.add('theme-auto', actualTheme)
    html.classList.add('theme-auto', actualTheme)
    console.log('🤖 自动主题，实际应用:', actualTheme)
  } else {
    body.classList.add(`theme-${theme}`)
    html.classList.add(`theme-${theme}`)
    console.log('✨ 应用主题类:', `theme-${theme}`)
  }
  
  // 输出当前类列表用于调试
  console.log('📋 body classes:', Array.from(body.classList))
  console.log('📋 html classes:', Array.from(html.classList))
  
  // 立即强制重绘
  document.documentElement.style.transition = 'all 0.3s ease'
  setTimeout(() => {
    document.documentElement.style.transition = ''
  }, 300)
}

function getThemeLabel(): string {
  const themeLabels: Record<string, string> = {
    'dark': '深色',
    'light': '浅色', 
    'auto': '自动',
    'blue': '深蓝',
    'purple': '紫色',
    'test': '测试'
  }
  return themeLabels[currentTheme.value] || '深色'
}

// 点击外部关闭主题菜单
function handleClickOutside(event: Event) {
  const target = event.target as Element
  if (!target.closest('.theme-switcher')) {
    showThemeMenu.value = false
  }
}
</script>

<style scoped>
/* 悬停动画效果 */
.animate-fadeIn {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 玻璃态效果 */
.glass-card {
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

/* 微信二维码悬停容器的特殊效果 */
.group:hover .group-hover\:block {
  animation: slideDown 0.3s ease-out;
}

.wechat-qr-card {
  min-width: 140px;
  animation: slideDown 0.3s ease-out;
}

/* 优化悬停区域，保持显示状态 */
.group:hover .wechat-qr-card,
.wechat-qr-card:hover {
  display: block !important;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-15px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* 微信图标的特殊样式 */
.group:hover svg {
  color: #10b981; /* 微信绿色 */
  transition: color 0.2s ease;
}

/* 保持二维码图片的正方形比例 */
.wechat-qr-card img {
  object-fit: contain;
  width: 128px;
  height: 128px;
}

/* 文本行限制 */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 数字动画 */
@keyframes countUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.animate-count-up {
  animation: countUp 0.6s ease-out;
}

/* 悬停渐变效果 */
.hover-gradient {
  position: relative;
  overflow: hidden;
}

.hover-gradient::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transition: left 0.5s;
}

.hover-gradient:hover::before {
  left: 100%;
}

/* 主题样式 */
/* 深色主题（默认） */
.theme-dark,
.theme-auto.theme-dark {
  /* 保持原有深色样式 */
}

/* 浅色主题 */
.theme-light,
.theme-auto.theme-light {
  background: linear-gradient(to bottom right, #f8fafc, #e2e8f0) !important;
}

.theme-light .bg-gradient-to-br,
.theme-auto.theme-light .bg-gradient-to-br {
  background: linear-gradient(to bottom right, #f8fafc, #e2e8f0) !important;
}

/* 浅色主题基础配色优化 */
.theme-light,
.theme-auto.theme-light {
  background: linear-gradient(to bottom right, #f8fafc, #e2e8f0) !important;
  color: #0f172a !important;
}

/* 浅色主题文字颜色优化 */
.theme-light .text-slate-100,
.theme-light .text-white,
.theme-auto.theme-light .text-slate-100,
.theme-auto.theme-light .text-white {
  color: #0f172a !important;
}

.theme-light .text-slate-300,
.theme-auto.theme-light .text-slate-300 {
  color: #334155 !important;
}

.theme-light .text-slate-400,
.theme-auto.theme-light .text-slate-400 {
  color: #475569 !important;
}

/* 浅色主题卡片样式优化 */
.theme-light .glass-card,
.theme-auto.theme-light .glass-card {
  background: rgba(255, 255, 255, 0.95) !important;
  border-color: rgba(148, 163, 184, 0.5) !important;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
  backdrop-filter: blur(10px) !important;
}

.theme-light .border-slate-600,
.theme-auto.theme-light .border-slate-600 {
  border-color: rgba(148, 163, 184, 0.5) !important;
}

/* 浅色主题悬停效果增强 */
.theme-light .glass-card:hover,
.theme-auto.theme-light .glass-card:hover {
  background: rgba(255, 255, 255, 0.98) !important;
  transform: translateY(-2px) scale(1.02) !important;
  box-shadow: 0 12px 20px -3px rgba(0, 0, 0, 0.15), 0 6px 8px -2px rgba(0, 0, 0, 0.08) !important;
  border-color: rgba(59, 130, 246, 0.4) !important;
}

/* 浅色主题背景卡片 */
.theme-light .bg-slate-800,
.theme-light .bg-slate-700,
.theme-auto.theme-light .bg-slate-800,
.theme-auto.theme-light .bg-slate-700 {
  background-color: rgba(255, 255, 255, 0.9) !important;
  border: 1px solid rgba(148, 163, 184, 0.4) !important;
  color: #0f172a !important;
}

.theme-light .bg-slate-800\/50,
.theme-light .bg-slate-700\/50,
.theme-auto.theme-light .bg-slate-800\/50,
.theme-auto.theme-light .bg-slate-700\/50 {
  background-color: rgba(248, 250, 252, 0.95) !important;
  border: 1px solid rgba(148, 163, 184, 0.4) !important;
  color: #0f172a !important;
}

/* 浅色主题下拉菜单优化 */
.theme-light .bg-slate-800\/90,
.theme-auto.theme-light .bg-slate-800\/90 {
  background: rgba(255, 255, 255, 0.96) !important;
  border: 1px solid rgba(148, 163, 184, 0.4) !important;
  color: #0f172a !important;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05) !important;
}

.theme-light .text-slate-200,
.theme-auto.theme-light .text-slate-200 {
  color: #334155 !important;
}

/* 浅色主题渐变文字增强 */
.theme-light h1 span,
.theme-auto.theme-light h1 span {
  background: linear-gradient(90deg, #2563eb, #7c3aed, #db2777) !important;
  background-clip: text !important;
  -webkit-background-clip: text !important;
  color: transparent !important;
  font-weight: 700 !important;
}

/* 浅色主题粒子效果调整 */
.theme-light .bg-blue-500\/20,
.theme-light .bg-purple-500\/20,
.theme-light .bg-pink-500\/20,
.theme-auto.theme-light .bg-blue-500\/20,
.theme-auto.theme-light .bg-purple-500\/20,
.theme-auto.theme-light .bg-pink-500\/20 {
  background-color: rgba(59, 130, 246, 0.08) !important;
}

/* 浅色主题统计卡片渐变保持 */
.theme-light .bg-gradient-to-br.from-blue-500,
.theme-light .bg-gradient-to-br.from-purple-500,
.theme-light .bg-gradient-to-br.from-pink-500,
.theme-light .bg-gradient-to-br.from-green-500,
.theme-auto.theme-light .bg-gradient-to-br.from-blue-500,
.theme-auto.theme-light .bg-gradient-to-br.from-purple-500,
.theme-auto.theme-light .bg-gradient-to-br.from-pink-500,
.theme-auto.theme-light .bg-gradient-to-br.from-green-500 {
  opacity: 0.95;
}

/* 浅色主题输入框优化 */
.theme-light input,
.theme-light select,
.theme-auto.theme-light input,
.theme-auto.theme-light select {
  color: #0f172a !important;
  background: rgba(255, 255, 255, 0.8) !important;
}

.theme-light input::placeholder,
.theme-auto.theme-light input::placeholder {
  color: #64748b !important;
}

/* 浅色主题按钮边框颜色优化 */
.theme-light .hover\:border-blue-400\/50:hover,
.theme-auto.theme-light .hover\:border-blue-400\/50:hover {
  border-color: rgba(59, 130, 246, 0.6) !important;
}

.theme-light .hover\:border-purple-400\/50:hover,
.theme-auto.theme-light .hover\:border-purple-400\/50:hover {
  border-color: rgba(147, 51, 234, 0.6) !important;
}

.theme-light .hover\:border-green-400\/50:hover,
.theme-auto.theme-light .hover\:border-green-400\/50:hover {
  border-color: rgba(34, 197, 94, 0.6) !important;
}

.theme-light .hover\:border-yellow-400\/50:hover,
.theme-auto.theme-light .hover\:border-yellow-400\/50:hover {
  border-color: rgba(250, 204, 21, 0.6) !important;
}

/* 深蓝主题 */
.theme-blue {
  background: linear-gradient(to bottom right, #0c1426, #1e2a4a) !important;
}

.theme-blue .bg-gradient-to-br {
  background: linear-gradient(to bottom right, #0c1426, #1e2a4a) !important;
}

.theme-blue .glass-card {
  background: rgba(12, 20, 38, 0.8) !important;
  border-color: rgba(184, 197, 214, 0.2) !important;
}

.theme-blue .bg-slate-800,
.theme-blue .bg-slate-700 {
  background-color: rgba(30, 42, 74, 0.6) !important;
}

/* 紫色主题 */
.theme-purple {
  background: linear-gradient(to bottom right, #1a0b2e, #2d1b4e) !important;
}

.theme-purple .bg-gradient-to-br {
  background: linear-gradient(to bottom right, #1a0b2e, #2d1b4e) !important;
}

.theme-purple .glass-card {
  background: rgba(26, 11, 46, 0.8) !important;
  border-color: rgba(209, 194, 232, 0.2) !important;
}

.theme-purple .bg-slate-800,
.theme-purple .bg-slate-700 {
  background-color: rgba(45, 27, 78, 0.6) !important;
}

.theme-purple .text-slate-100,
.theme-purple .text-white {
  color: #f0e6ff !important;
}

.theme-purple .text-slate-300 {
  color: #d1c2e8 !important;
}

.theme-purple .text-slate-400 {
  color: #b299d1 !important;
}

/* 测试主题 - 非常明显的红色 */
.theme-test {
  background: linear-gradient(to bottom right, #dc2626, #991b1b) !important;
}

.theme-test .bg-gradient-to-br {
  background: linear-gradient(to bottom right, #dc2626, #991b1b) !important;
}

.theme-test .glass-card {
  background: rgba(220, 38, 38, 0.8) !important;
  border-color: rgba(255, 255, 255, 0.3) !important;
}

.theme-test .bg-slate-800,
.theme-test .bg-slate-700 {
  background-color: rgba(153, 27, 27, 0.6) !important;
}

.theme-test .text-slate-100,
.theme-test .text-white {
  color: #fef2f2 !important;
}

.theme-test .text-slate-300 {
  color: #fecaca !important;
}

.theme-test .text-slate-400 {
  color: #fca5a5 !important;
}

/* 主题切换动画 */
.theme-transition {
  transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}

/* 主题切换按钮特殊样式 */
.theme-switcher {
  position: relative;
}

.theme-menu-item:hover {
  background: rgba(var(--rgb-slate-700), 0.5);
}

/* 自定义滚动条（适应主题） */
.theme-light ::-webkit-scrollbar {
  width: 8px;
}

.theme-light ::-webkit-scrollbar-track {
  background: var(--bg-secondary);
}

.theme-light ::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 4px;
}

.theme-light ::-webkit-scrollbar-thumb:hover {
  background: var(--text-muted);
}
</style>