<template>
  <div class="bg-gradient-to-br from-slate-800 to-slate-900 text-slate-100 min-h-screen font-sans">
    <!-- 测试内容 -->
    <div class="container mx-auto px-4 py-12">
      <h1 class="text-4xl font-bold text-center mb-8">
        <span style="background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899); background-clip: text; -webkit-background-clip: text; color: transparent;">
          GitHub每周热门项目
        </span>
      </h1>
      
      <div class="text-center mb-8">
        <p class="text-slate-400 text-lg">正在加载数据...</p>
      </div>
      
      <!-- 显示加载状态 -->
      <div v-if="loading" class="text-center py-16">
        <div class="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
        <p class="text-slate-400">加载报告中...</p>
      </div>
      
      <!-- 显示错误 -->
      <div v-else-if="error" class="text-center py-20">
        <div class="text-red-400 text-lg mb-4">加载失败</div>
        <p class="text-slate-400">{{ error }}</p>
        <button @click="fetchReports" class="mt-4 bg-blue-500 text-white px-4 py-2 rounded">重试</button>
      </div>
      
      <!-- 显示报告列表 -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div 
          v-for="report in reports" 
          :key="report.date"
          class="bg-slate-800/50 rounded-lg p-6 border border-slate-600 hover:border-blue-500 transition-colors cursor-pointer"
          @click="openReport(report.date)"
        >
          <div class="text-lg font-semibold mb-2">{{ report.date }}</div>
          <div class="text-slate-400">{{ report.project_count }} 个项目</div>
        </div>
      </div>
      
      <!-- API 状态信息 -->
      <div class="mt-8 text-center text-slate-500 text-sm">
        API 地址: {{ API_BASE_URL }}
      </div>
    </div>
  </div>
</template>

      <!-- 日期卡片网格 -->
      <section class="mb-16">
        <div class="flex flex-col space-y-4 lg:space-y-0 lg:flex-row justify-between items-start lg:items-center mb-6 lg:mb-8 gap-4">
          <h3 class="text-xl lg:text-2xl font-bold">报告列表</h3>
          <div class="flex flex-col sm:flex-row gap-2 lg:gap-3 w-full lg:w-auto">
            <!-- 搜索框 -->
            <div class="relative flex-1 lg:flex-none">
              <input 
                type="text" 
                v-model="searchFilter"
                placeholder="搜索日期、项目数量..." 
                class="bg-slate-800/50 border border-white/10 rounded-lg px-4 py-2 pl-10 pr-12 focus:outline-none focus:ring-2 focus:ring-blue-500 w-full lg:w-80 transition-all duration-200 text-sm lg:text-base"
                @input="handleSearch"
              >
              <i class="fa fa-search absolute left-3 top-2.5 lg:top-3 text-slate-400"></i>
              <button 
                v-if="searchFilter" 
                @click="clearSearch" 
                class="absolute right-3 top-2 lg:top-2.5 text-slate-400 hover:text-white transition-colors"
              >
                <i class="fa fa-times"></i>
              </button>
            </div>
            
            <!-- 排序选择 -->
            <div class="relative">
              <select 
                v-model="sortOrder" 
                class="bg-slate-800/50 border border-white/10 rounded-lg px-3 lg:px-4 py-2 pr-8 focus:outline-none focus:ring-2 focus:ring-blue-500 appearance-none cursor-pointer text-sm lg:text-base w-full lg:w-auto"
              >
                <option value="desc">最新优先</option>
                <option value="asc">最早优先</option>
                <option value="projects">项目数量</option>
              </select>
              <i class="fa fa-chevron-down absolute right-3 top-2.5 lg:top-3 text-slate-400 pointer-events-none"></i>
            </div>
            
            <!-- 显示数量 -->
            <div class="relative">
              <select 
                v-model="displayLimit" 
                class="bg-slate-800/50 border border-white/10 rounded-lg px-3 lg:px-4 py-2 pr-8 focus:outline-none focus:ring-2 focus:ring-blue-500 appearance-none cursor-pointer text-sm lg:text-base w-full lg:w-auto"
              >
                <option :value="12">显示 12 个</option>
                <option :value="24">显示 24 个</option>
                <option :value="48">显示 48 个</option>
                <option :value="0">显示全部</option>
              </select>
              <i class="fa fa-chevron-down absolute right-3 top-2.5 lg:top-3 text-slate-400 pointer-events-none"></i>
            </div>
            
            <!-- 快速筛选 -->
            <button 
              @click="toggleFilters" 
              class="bg-purple-500/20 text-purple-300 border border-purple-500/30 px-3 lg:px-4 py-2 rounded-lg hover:bg-purple-500/30 transition-all duration-200 flex items-center justify-center text-sm lg:text-base"
            >
              <i class="fa fa-filter mr-2"></i>
              筛选
            </button>
          </div>
        </div>
        
        <!-- 高级筛选面板 -->
        <div v-if="showFilters" class="mb-6 lg:mb-8 p-4 lg:p-6 bg-slate-800/30 rounded-xl border border-slate-600/30 animate-fadeIn">
          <!-- 快速筛选按钮 -->
          <div class="mb-4 lg:mb-6">
            <h4 class="text-sm font-medium text-slate-300 mb-3">快速筛选</h4>
            <div class="flex flex-wrap gap-2">
              <button @click="quickFilterByDate(7)" class="bg-blue-500/20 text-blue-300 border border-blue-500/30 px-2 lg:px-3 py-1 lg:py-1.5 rounded-lg text-xs hover:bg-blue-500/30 transition-all">近7天</button>
              <button @click="quickFilterByDate(30)" class="bg-blue-500/20 text-blue-300 border border-blue-500/30 px-2 lg:px-3 py-1 lg:py-1.5 rounded-lg text-xs hover:bg-blue-500/30 transition-all">近30天</button>
              <button @click="quickFilterByDate(90)" class="bg-blue-500/20 text-blue-300 border border-blue-500/30 px-2 lg:px-3 py-1 lg:py-1.5 rounded-lg text-xs hover:bg-blue-500/30 transition-all">近90天</button>
              <button @click="quickFilterByProjects(10)" class="bg-purple-500/20 text-purple-300 border border-purple-500/30 px-2 lg:px-3 py-1 lg:py-1.5 rounded-lg text-xs hover:bg-purple-500/30 transition-all">10+项目</button>
              <button @click="quickFilterByProjects(20)" class="bg-purple-500/20 text-purple-300 border border-purple-500/30 px-2 lg:px-3 py-1 lg:py-1.5 rounded-lg text-xs hover:bg-purple-500/30 transition-all">20+项目</button>
              <button @click="quickFilterByProjects(50)" class="bg-purple-500/20 text-purple-300 border border-purple-500/30 px-2 lg:px-3 py-1 lg:py-1.5 rounded-lg text-xs hover:bg-purple-500/30 transition-all">50+项目</button>
            </div>
          </div>
          
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 lg:gap-6">
            <div>
              <label class="block text-sm font-medium text-slate-300 mb-2">日期范围</label>
              <div class="flex flex-col sm:flex-row gap-2">
                <input 
                  type="date" 
                  v-model="dateFilter.start"
                  class="bg-slate-700/50 border border-slate-600 rounded-lg px-3 py-2 text-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500 flex-1 text-sm"
                >
                <span class="text-slate-400 self-center text-center sm:text-left text-sm">至</span>
                <input 
                  type="date" 
                  v-model="dateFilter.end"
                  class="bg-slate-700/50 border border-slate-600 rounded-lg px-3 py-2 text-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500 flex-1 text-sm"
                >
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-slate-300 mb-2">项目数量范围</label>
              <div class="flex flex-col sm:flex-row gap-2">
                <input 
                  type="number" 
                  v-model.number="projectFilter.min"
                  placeholder="最少"
                  class="bg-slate-700/50 border border-slate-600 rounded-lg px-3 py-2 text-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500 flex-1 text-sm"
                >
                <span class="text-slate-400 self-center text-center sm:text-left text-sm">~</span>
                <input 
                  type="number" 
                  v-model.number="projectFilter.max"
                  placeholder="最多"
                  class="bg-slate-700/50 border border-slate-600 rounded-lg px-3 py-2 text-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500 flex-1 text-sm"
                >
              </div>
            </div>
            
            <div class="flex items-end">
              <button 
                @click="resetFilters" 
                class="bg-slate-600/50 text-slate-300 border border-slate-500 px-4 py-2 rounded-lg hover:bg-slate-600/70 transition-all duration-200 w-full text-sm"
              >
                <i class="fa fa-refresh mr-2"></i>
                重置筛选
              </button>
            </div>
          </div>
        </div>
        
        <!-- 加载状态 -->
        <div v-if="loading" class="text-center py-16">
          <div class="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p class="text-slate-400">加载报告中...</p>
        </div>
        
        <!-- 错误状态 -->
        <div v-else-if="error" class="text-center py-20 animate-fadeIn">
          <div class="max-w-md mx-auto glass-card rounded-2xl p-8">
            <div class="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg class="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-red-400 mb-4">加载失败</h3>
            <p class="text-slate-400 mb-6">{{ error }}</p>
            <div class="flex space-x-3 justify-center">
              <button @click="fetchReports" class="btn-primary">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                </svg>
                重试
              </button>
              <button @click="checkConnection" class="btn-secondary">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                </svg>
                检查连接
              </button>
            </div>
          </div>
        </div>
        
        <!-- 空数据状态 -->
        <div v-else-if="filteredReports.length === 0" class="text-center py-20 animate-fadeIn">
          <div class="max-w-md mx-auto">
            <div class="w-24 h-24 bg-slate-700/50 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg class="w-12 h-12 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-slate-300 mb-4">暂无报告</h3>
            <p class="text-slate-400 mb-6">
              {{ searchFilter ? '没有找到匹配的报告' : '还没有生成任何报告' }}
            </p>
            <div class="flex justify-center space-x-3">
              <button v-if="searchFilter" @click="searchFilter = ''" class="btn-secondary">
                清除搜索
              </button>
              <button @click="refreshData" class="btn-primary">
                刷新数据
              </button>
            </div>
          </div>
        </div>
        
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
          <div 
            v-for="(report, index) in filteredReports" 
            :key="report.date"
            class="report-card relative bg-gradient-to-br from-slate-800/60 to-slate-900/60 rounded-3xl overflow-hidden border border-white/10 hover:border-white/20 cursor-pointer animate-fadeInUp backdrop-blur-xl group transition-all duration-500 hover:transform hover:scale-105 hover:shadow-2xl"
            :style="{ animationDelay: `${index * 0.08}s` }"
            @click="openReport(report.date)"
            @mouseenter="previewReport(report.date)"
          >
            <!-- 背景装饰 -->
            <div class="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-bl from-blue-500/10 to-transparent rounded-full transform translate-x-8 -translate-y-8"></div>
            
            <!-- 最新标识 -->
            <div v-if="index === 0" class="absolute top-4 right-4 z-10">
              <div class="bg-gradient-to-r from-pink-500 to-rose-500 text-white text-xs px-3 py-1 rounded-full shadow-lg animate-pulse">
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
                      <i class="fa fa-arrow-right animate-bounce-x"></i>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- 快速操作按钮 -->
              <div class="flex gap-2 opacity-0 group-hover:opacity-100 transition-all duration-300 transform translate-y-2 group-hover:translate-y-0">
                <button 
                  @click.stop="openReport(report.date)"
                  class="flex-1 bg-gradient-to-r from-blue-500/20 to-blue-600/20 text-blue-300 border border-blue-500/30 px-3 py-2.5 rounded-xl text-xs font-semibold hover:from-blue-500/30 hover:to-blue-600/30 transition-all duration-200 flex items-center justify-center group/btn"
                >
                  <i class="fa fa-file-text mr-1.5 group-hover/btn:animate-pulse"></i>
                  详细报告
                </button>
                <button 
                  @click.stop="viewProjects(report.date)"
                  class="flex-1 bg-gradient-to-r from-purple-500/20 to-purple-600/20 text-purple-300 border border-purple-500/30 px-3 py-2.5 rounded-xl text-xs font-semibold hover:from-purple-500/30 hover:to-purple-600/30 transition-all duration-200 flex items-center justify-center group/btn"
                >
                  <i class="fa fa-th-list mr-1.5 group-hover/btn:animate-pulse"></i>
                  项目列表
                </button>
              </div>
            </div>
            
            <!-- 底部装饰线 -->
            <div class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 opacity-60 group-hover:opacity-100 transition-opacity duration-300"></div>
            
            <!-- 悬浮光晕效果 -->
            <div class="absolute inset-0 rounded-3xl bg-gradient-to-br from-blue-500/10 to-purple-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"></div>
          </div>
        </div>
      </section>

      <!-- 数据可视化图表 -->
      <section class="mb-16">
        <StatsChart :stats="stats" />
      </section>

      <!-- 筛选和搜索区域 -->
      <section class="mb-16">
        <div class="flex justify-between items-center mb-8">
          <h3 class="text-2xl font-bold">报告列表</h3>
          <div class="relative">
            <input 
              type="text" 
              v-model="searchFilter"
              placeholder="搜索日期 (YYYY-MM-DD)..." 
              class="bg-slate-800/50 border border-white/10 rounded-lg px-4 py-2 pl-10 focus:outline-none focus:ring-2 focus:ring-blue-500 w-full md:w-64"
            >
            <i class="fa fa-search absolute left-3 top-3 text-slate-400"></i>
          </div>
        </div>
        
        <!-- 加载状态 -->
        <div v-if="loading" class="text-center py-16">
          <div class="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p class="text-slate-400">加载报告中...</p>
        </div>
        
        <!-- 错误状态 -->
        <div v-else-if="error" class="text-center py-20 animate-fadeIn">
          <div class="max-w-md mx-auto glass-card rounded-2xl p-8">
            <div class="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg class="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-red-400 mb-4">加载失败</h3>
            <p class="text-slate-400 mb-6">{{ error }}</p>
            <div class="flex space-x-3 justify-center">
              <button @click="fetchReports" class="btn-primary">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                </svg>
                重试
              </button>
              <button @click="checkConnection" class="btn-secondary">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                </svg>
                检查连接
              </button>
            </div>
          </div>
        </div>
        
        <!-- 空数据状态 -->
        <div v-else-if="filteredReports.length === 0" class="text-center py-20 animate-fadeIn">
          <div class="max-w-md mx-auto">
            <div class="w-24 h-24 bg-slate-700/50 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg class="w-12 h-12 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-slate-300 mb-4">暂无报告</h3>
            <p class="text-slate-400 mb-6">
              {{ searchFilter ? '没有找到匹配的报告' : '还没有生成任何报告' }}
            </p>
            <div class="flex justify-center space-x-3">
              <button v-if="searchFilter" @click="searchFilter = ''" class="btn-secondary">
                清除搜索
              </button>
              <button @click="refreshData" class="btn-primary">
                刷新数据
              </button>
            </div>
          </div>
        </div>
        
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <div 
            v-for="(report, index) in filteredReports" 
            :key="report.date"
            class="date-card bg-slate-800/50 rounded-2xl overflow-hidden card-border hover-lift cursor-pointer animate-fadeInUp backdrop-blur-sm group"
            :style="{ animationDelay: `${index * 0.05}s` }"
          >
            <div class="p-6">
              <div class="flex justify-between items-start mb-4">
                <div>
                  <div class="text-slate-400 text-sm">{{ formatDateShort(report.date) }}</div>
                  <div class="text-3xl font-bold mt-1">{{ formatDay(report.date) }}</div>
                </div>
                <span v-if="index === 0" class="bg-pink-500/20 text-pink-400 text-xs px-2 py-1 rounded-full">
                  最新
                </span>
              </div>
              <div class="flex items-center text-slate-300 mb-5">
                <i class="fa fa-cube mr-2 text-blue-500"></i>
                <span>{{ report.project_count }} 个项目</span>
              </div>
              
              <!-- 操作按钮组 -->
              <div class="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                <button 
                  @click.stop="openReport(report.date)"
                  class="flex-1 bg-blue-500/20 text-blue-400 border border-blue-500/30 px-3 py-2 rounded-lg text-xs font-medium hover:bg-blue-500/30 transition-colors flex items-center justify-center"
                >
                  <i class="fa fa-file-text mr-1"></i>
                  查看报告
                </button>
                <button 
                  @click.stop="viewProjects(report.date)"
                  class="flex-1 bg-purple-500/20 text-purple-400 border border-purple-500/30 px-3 py-2 rounded-lg text-xs font-medium hover:bg-purple-500/30 transition-colors flex items-center justify-center"
                >
                  <i class="fa fa-th-list mr-1"></i>
                  查看项目
                </button>
              </div>
            </div>
            <div class="h-1 bg-gradient-to-r from-blue-500 to-purple-600"></div>
          </div>
        </div>
      </section>
    </main>

    <!-- 报告详情模态框 -->
    <ReportModal 
      v-if="selectedReport" 
      :report="selectedReport" 
      @close="closeReport" 
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getReports, type Report } from '../api/reports'

// 响应式数据
const reports = ref<Report[]>([])
const loading = ref(true)
const error = ref<string | null>(null)
const API_BASE_URL = 'http://localhost:5002'

// 获取报告列表
async function fetchReports() {
  try {
    loading.value = true
    error.value = null
    console.log('开始获取报告...')
    reports.value = await getReports()
    console.log('报告获取成功:', reports.value)
  } catch (err: any) {
    error.value = err.message || '获取报告列表失败'
    console.error('获取报告失败:', err)
  } finally {
    loading.value = false
  }
}

// 打开报告
function openReport(date: string) {
  console.log('打开报告:', date)
  // 这里可以添加报告详情逻辑
}

// 组件挂载时获取数据
onMounted(() => {
  console.log('组件已挂载，开始获取数据')
  fetchReports()
})
</script>

// Icons as components
const ChartBarIcon = {
  template: `<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
  </svg>`
}

const CubeIcon = {
  template: `<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
  </svg>`
}

const CodeIcon = {
  template: `<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
  </svg>`
}

const TrendingUpIcon = {
  template: `<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
  </svg>`
}

const router = useRouter()

// 响应式数据
const reports = ref<Report[]>([])
const stats = ref<Stats>({ 
  totalReports: 0, 
  totalProjects: 0, 
  topLanguage: 'N/A', 
  weeklyNew: 0, 
  totalForks: '0', 
  avgContributors: 0 
})
const selectedReport = ref<Report | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)
const searchFilter = ref('')
const showFilters = ref(false)
const sortOrder = ref('desc')
const displayLimit = ref(12)
const connectionStatus = ref(false)
const lastUpdate = ref<Date | null>(null)

// 高级筛选功能
const dateFilter = ref({
  start: '',
  end: ''
})
const projectFilter = ref({
  min: null as number | null,
  max: null as number | null
})
const searchResults = ref<Report[]>([])
const isSearching = ref(false)

// 统计卡片配置
const statsConfig = computed(() => [
  {
    key: 'totalReports',
    label: '总报告数',
    icon: ChartBarIcon,
    bgClass: 'bg-gradient-to-br from-blue-500 to-blue-600',
    badgeClass: 'bg-blue-500/20 text-blue-400',
    badge: '报告',
    description: '累计生成'
  },
  {
    key: 'totalProjects',
    label: '总项目数',
    icon: CubeIcon,
    bgClass: 'bg-gradient-to-br from-purple-500 to-purple-600',
    badgeClass: 'bg-purple-500/20 text-purple-400',
    badge: '项目',
    description: '已分析'
  },
  {
    key: 'topLanguage',
    label: '热门语言',
    icon: CodeIcon,
    bgClass: 'bg-gradient-to-br from-pink-500 to-pink-600',
    badgeClass: 'bg-pink-500/20 text-pink-400',
    badge: '语言',
    description: '最受欢迎'
  },
  {
    key: 'weeklyNew',
    label: '本周新增',
    icon: TrendingUpIcon,
    bgClass: 'bg-gradient-to-br from-green-500 to-green-600',
    badgeClass: 'bg-green-500/20 text-green-400',
    badge: '新增',
    description: '迗日统计'
  }
])

// 计算属性
const latestDate = computed(() => {
  if (reports.value.length === 0) return '暂无'
  const latest = reports.value[0].date
  return formatDate(latest)
})

const filteredReports = computed(() => {
  let filtered = reports.value
  
  // 搜索过滤（支持日期和项目数量搜索）
  if (searchFilter.value.trim()) {
    const searchTerm = searchFilter.value.trim().toLowerCase()
    filtered = filtered.filter(report => {
      return report.date.toLowerCase().includes(searchTerm) ||
             report.project_count.toString().includes(searchTerm) ||
             formatDateShort(report.date).toLowerCase().includes(searchTerm) ||
             formatDateWeek(report.date).toLowerCase().includes(searchTerm)
    })
  }
  
  // 日期范围过滤
  if (dateFilter.value.start) {
    filtered = filtered.filter(report => report.date >= dateFilter.value.start)
  }
  if (dateFilter.value.end) {
    filtered = filtered.filter(report => report.date <= dateFilter.value.end)
  }
  
  // 项目数量过滤
  if (projectFilter.value.min !== null) {
    filtered = filtered.filter(report => report.project_count >= projectFilter.value.min!)
  }
  if (projectFilter.value.max !== null) {
    filtered = filtered.filter(report => report.project_count <= projectFilter.value.max!)
  }
  
  // 排序
  if (sortOrder.value === 'asc') {
    filtered = [...filtered].sort((a, b) => a.date.localeCompare(b.date))
  } else if (sortOrder.value === 'desc') {
    filtered = [...filtered].sort((a, b) => b.date.localeCompare(a.date))
  } else if (sortOrder.value === 'projects') {
    filtered = [...filtered].sort((a, b) => b.project_count - a.project_count)
  }
  
  // 显示数量限制
  if (displayLimit.value > 0) {
    filtered = filtered.slice(0, displayLimit.value)
  }
  
  return filtered
})

// 生命周期钩子
onMounted(async () => {
  await initializeApp()
  startHealthCheck()
})

onUnmounted(() => {
  stopHealthCheck()
})

// 健康检查定时器
let healthCheckInterval: NodeJS.Timeout | null = null

function startHealthCheck() {
  checkConnection()
  healthCheckInterval = setInterval(checkConnection, 30000) // 每30秒检查一次
}

function stopHealthCheck() {
  if (healthCheckInterval) {
    clearInterval(healthCheckInterval)
    healthCheckInterval = null
  }
}

// 初始化应用
async function initializeApp() {
  console.log(`🌐 连接到 API: ${getApiBaseUrl()}`)
  await Promise.all([
    fetchReports(),
    fetchStats()
  ])
}

// 检查连接状态
async function checkConnection() {
  try {
    connectionStatus.value = await healthCheck()
  } catch {
    connectionStatus.value = false
  }
}

// 刷新数据
async function refreshData() {
  await Promise.all([
    fetchReports(),
    fetchStats()
  ])
}

// 方法
async function fetchReports() {
  try {
    loading.value = true
    error.value = null
    reports.value = await getReports()
    lastUpdate.value = new Date()
    console.log(`📊 成功加载 ${reports.value.length} 个报告`)
  } catch (err: any) {
    error.value = err.message || '获取报告列表失败'
    console.error('获取报告列表失败:', err)
  } finally {
    loading.value = false
  }
}

async function fetchStats() {
  try {
    const newStats = await reportApi.getStats()
    stats.value = newStats
    console.log('📊 统计数据更新成功')
  } catch (err: any) {
    console.error('获取统计数据失败:', err)
    // 不显示错误，保持现有数据
  }
}

async function openReport(date: string) {
  try {
    const report = await reportApi.getReportContent(date)
    selectedReport.value = report
    console.log(`📄 打开报告: ${date}`)
  } catch (err: any) {
    error.value = err.message || '获取报告详情失败'
    console.error('获取报告详情失败:', err)
  }
}

function closeReport() {
  selectedReport.value = null
}

function viewProjects(date: string) {
  router.push(`/projects/${date}`)
}

// 导出数据
function exportData() {
  const dataToExport = {
    stats: stats.value,
    reports: filteredReports.value,
    exportTime: new Date().toISOString(),
    totalCount: reports.value.length
  }
  
  const blob = new Blob([JSON.stringify(dataToExport, null, 2)], {
    type: 'application/json'
  })
  
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `github-trending-reports-${new Date().toISOString().split('T')[0]}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
  
  console.log('📥 数据导出成功')
}

// 格式化函数
function formatStatValue(key: string): string {
  const value = stats.value[key as keyof Stats]
  if (typeof value === 'number') {
    return value.toLocaleString()
  }
  return String(value)
}

function formatLastUpdate(): string {
  if (!lastUpdate.value) return '从未更新'
  const now = new Date()
  const diff = now.getTime() - lastUpdate.value.getTime()
  const minutes = Math.floor(diff / 60000)
  
  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours}小时前`
  
  const days = Math.floor(hours / 24)
  return `${days}天前`
}

function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  })
}

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

// 新增的功能函数
function handleSearch() {
  // 实时搜索，无需额外处理，计算属性会自动响应
}

function clearSearch() {
  searchFilter.value = ''
}

function toggleFilters() {
  showFilters.value = !showFilters.value
}

function resetFilters() {
  dateFilter.value.start = ''
  dateFilter.value.end = ''
  projectFilter.value.min = null
  projectFilter.value.max = null
  searchFilter.value = ''
  sortOrder.value = 'desc'
  displayLimit.value = 12
}

// 快速操作功能
function quickFilterByDate(days: number) {
  const endDate = new Date()
  const startDate = new Date()
  startDate.setDate(endDate.getDate() - days)
  
  dateFilter.value.start = startDate.toISOString().split('T')[0]
  dateFilter.value.end = endDate.toISOString().split('T')[0]
}

function quickFilterByProjects(min: number, max?: number) {
  projectFilter.value.min = min
  projectFilter.value.max = max || null
}

// 预览功能
function previewReport(date: string) {
  // 快速预览报告内容（前200个字符）
  reportApi.getReportContent(date).then(report => {
    if (report.content) {
      const preview = report.content.substring(0, 200) + '...'
      showTooltip(preview, event?.target as HTMLElement)
    }
  }).catch(console.error)
}

function showTooltip(content: string, target: HTMLElement) {
  // 创建简单的提示框
  const tooltip = document.createElement('div')
  tooltip.className = 'fixed z-50 bg-slate-800 border border-slate-600 rounded-lg p-3 text-sm text-slate-300 max-w-xs shadow-xl'
  tooltip.textContent = content
  
  document.body.appendChild(tooltip)
  
  // 定位提示框
  const rect = target.getBoundingClientRect()
  tooltip.style.left = rect.left + 'px'
  tooltip.style.top = (rect.bottom + 10) + 'px'
  
  // 3秒后自动移除
  setTimeout(() => {
    if (document.body.contains(tooltip)) {
      document.body.removeChild(tooltip)
    }
  }, 3000)
  
  // 点击其他地方移除提示框
  const removeTooltip = () => {
    if (document.body.contains(tooltip)) {
      document.body.removeChild(tooltip)
    }
    document.removeEventListener('click', removeTooltip)
  }
  
  setTimeout(() => {
    document.addEventListener('click', removeTooltip)
  }, 100)
}

</script>