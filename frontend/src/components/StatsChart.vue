<template>
  <div class="stats-chart glass-card rounded-2xl p-6">
    <h3 style="background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899); background-clip: text; -webkit-background-clip: text; color: transparent;" class="text-xl font-bold mb-6">数据统计概览</h3>
    
    <!-- 统计卡片网格 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <div 
        v-for="(stat, index) in statsData" 
        :key="stat.key"
        class="stat-card glass-card rounded-xl p-4 hover-lift-sm animate-fadeInUp"
        :style="{ animationDelay: `${index * 0.1}s` }"
      >
        <div class="flex items-center justify-between mb-3">
          <div :class="['p-2 rounded-lg', stat.bgClass]">
            <component :is="stat.icon" class="w-5 h-5 text-white" />
          </div>
          <div :class="['text-xs px-2 py-1 rounded-full', stat.badgeClass]">
            {{ stat.change }}
          </div>
        </div>
        <div class="text-2xl font-bold text-white mb-1">{{ stat.value }}</div>
        <div class="text-sm text-slate-400">{{ stat.label }}</div>
        <div class="mt-2 w-full bg-slate-700/50 rounded-full h-1">
          <div 
            :class="['h-full rounded-full transition-all duration-500', stat.progressClass]"
            :style="{ width: stat.progress + '%' }"
          ></div>
        </div>
      </div>
    </div>
    
    <!-- 简单的条形图 -->
    <div class="mb-6">
      <h4 class="text-lg font-semibold text-slate-300 mb-4">编程语言分布</h4>
      <div class="space-y-3">
        <div 
          v-for="(lang, index) in languageData" 
          :key="lang.name"
          class="flex items-center space-x-3 animate-slideIn"
          :style="{ animationDelay: `${index * 0.1 + 0.5}s` }"
        >
          <div class="flex-shrink-0 w-20 text-sm text-slate-400 font-medium">
            {{ lang.name }}
          </div>
          <div class="flex-grow bg-slate-700/50 rounded-full h-3 relative overflow-hidden">
            <div 
              class="h-full rounded-full transition-all duration-700 ease-out"
              :class="lang.colorClass"
              :style="{ width: lang.percentage + '%' }"
            ></div>
          </div>
          <div class="flex-shrink-0 w-12 text-sm text-slate-300 text-right">
            {{ lang.percentage }}%
          </div>
        </div>
      </div>
    </div>
    
    <!-- 趋势指标 -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="space-y-4">
        <h4 class="text-lg font-semibold text-slate-300">项目趋势</h4>
        <div class="space-y-3">
          <div 
            v-for="(trend, index) in trendData" 
            :key="trend.label"
            class="flex items-center justify-between p-3 bg-slate-800/30 rounded-lg animate-fadeInUp"
            :style="{ animationDelay: `${index * 0.1 + 0.8}s` }"
          >
            <div class="flex items-center space-x-3">
              <div :class="['w-2 h-2 rounded-full', trend.colorClass]"></div>
              <span class="text-sm text-slate-300">{{ trend.label }}</span>
            </div>
            <div class="flex items-center space-x-2">
              <span class="text-sm font-medium text-white">{{ trend.value }}</span>
              <svg 
                v-if="trend.change > 0" 
                class="w-4 h-4 text-green-400" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
              </svg>
              <svg 
                v-else-if="trend.change < 0" 
                class="w-4 h-4 text-red-400" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6"></path>
              </svg>
              <svg 
                v-else 
                class="w-4 h-4 text-gray-400" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>
      
      <div class="space-y-4">
        <h4 class="text-lg font-semibold text-slate-300">活跃度分析</h4>
        <div class="relative">
          <!-- 简单的环形进度条 -->
          <div class="flex items-center justify-center">
            <div class="relative w-32 h-32">
              <svg class="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                <!-- 背景圆环 -->
                <circle
                  cx="50"
                  cy="50"
                  r="40"
                  stroke="rgb(51 65 85)"
                  stroke-width="8"
                  fill="none"
                />
                <!-- 进度圆环 -->
                <circle
                  cx="50"
                  cy="50"
                  r="40"
                  stroke="url(#gradient)"
                  stroke-width="8"
                  fill="none"
                  stroke-linecap="round"
                  :stroke-dasharray="`${activityScore * 2.51} 251`"
                  class="transition-all duration-1000 ease-out"
                />
                <!-- 渐变定义 -->
                <defs>
                  <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" style="stop-color:#3B82F6"/>
                    <stop offset="100%" style="stop-color:#8B5CF6"/>
                  </linearGradient>
                </defs>
              </svg>
              <div class="absolute inset-0 flex items-center justify-center">
                <div class="text-center">
                  <div class="text-2xl font-bold text-white">{{ activityScore }}%</div>
                  <div class="text-xs text-slate-400">活跃度</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type { Stats } from '../api/reports'

// Props
const props = defineProps<{
  stats: Stats
}>()

// Icons
const BarChartIcon = {
  template: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
  </svg>`
}

const CubeIcon = {
  template: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
  </svg>`
}

const CodeIcon = {
  template: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
  </svg>`
}

const TrendingUpIcon = {
  template: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
  </svg>`
}

// 响应式数据
const activityScore = ref(0)

// 计算属性
const statsData = computed(() => [
  {
    key: 'totalReports',
    label: '总报告数',
    value: props.stats.totalReports.toLocaleString(),
    icon: BarChartIcon,
    bgClass: 'bg-gradient-to-br from-blue-500 to-blue-600',
    badgeClass: 'bg-blue-500/20 text-blue-400',
    progressClass: 'bg-gradient-to-r from-blue-500 to-blue-600',
    change: '+12%',
    progress: Math.min(100, (props.stats.totalReports / 50) * 100)
  },
  {
    key: 'totalProjects',
    label: '总项目数',
    value: props.stats.totalProjects.toLocaleString(),
    icon: CubeIcon,
    bgClass: 'bg-gradient-to-br from-purple-500 to-purple-600',
    badgeClass: 'bg-purple-500/20 text-purple-400',
    progressClass: 'bg-gradient-to-r from-purple-500 to-purple-600',
    change: '+8%',
    progress: Math.min(100, (props.stats.totalProjects / 100) * 100)
  },
  {
    key: 'weeklyNew',
    label: '本周新增',
    value: props.stats.weeklyNew.toLocaleString(),
    icon: TrendingUpIcon,
    bgClass: 'bg-gradient-to-br from-green-500 to-green-600',
    badgeClass: 'bg-green-500/20 text-green-400',
    progressClass: 'bg-gradient-to-r from-green-500 to-green-600',
    change: '+15%',
    progress: Math.min(100, (props.stats.weeklyNew / 20) * 100)
  },
  {
    key: 'avgContributors',
    label: '平均贡献者',
    value: Math.round(props.stats.avgContributors).toLocaleString(),
    icon: CodeIcon,
    bgClass: 'bg-gradient-to-br from-orange-500 to-orange-600',
    badgeClass: 'bg-orange-500/20 text-orange-400',
    progressClass: 'bg-gradient-to-r from-orange-500 to-orange-600',
    change: '+3%',
    progress: Math.min(100, (props.stats.avgContributors / 200) * 100)
  }
])

const languageData = computed(() => {
  // 模拟语言分布数据
  const languages = [
    { name: 'TypeScript', percentage: 35, colorClass: 'bg-gradient-to-r from-blue-500 to-blue-600' },
    { name: 'JavaScript', percentage: 28, colorClass: 'bg-gradient-to-r from-yellow-500 to-yellow-600' },
    { name: 'Python', percentage: 20, colorClass: 'bg-gradient-to-r from-green-500 to-green-600' },
    { name: 'Go', percentage: 10, colorClass: 'bg-gradient-to-r from-cyan-500 to-cyan-600' },
    { name: 'Rust', percentage: 7, colorClass: 'bg-gradient-to-r from-orange-500 to-orange-600' }
  ]
  return languages
})

const trendData = computed(() => [
  { label: '新项目', value: props.stats.weeklyNew, change: 1, colorClass: 'bg-green-400' },
  { label: '活跃项目', value: Math.round(props.stats.totalProjects * 0.3), change: 1, colorClass: 'bg-blue-400' },
  { label: '热门项目', value: Math.round(props.stats.totalProjects * 0.1), change: 0, colorClass: 'bg-purple-400' },
  { label: '趋势项目', value: Math.round(props.stats.totalProjects * 0.05), change: -1, colorClass: 'bg-pink-400' }
])

// 生命周期
onMounted(() => {
  // 动画延迟显示活跃度分数
  setTimeout(() => {
    activityScore.value = Math.round(75 + Math.random() * 20) // 75-95% 的随机活跃度
  }, 1000)
})
</script>