<template>
  <div class="bg-gradient-to-br from-slate-800 to-slate-900 text-slate-100 min-h-screen font-sans">
    <main class="container mx-auto px-4 py-12">
      <header class="text-center mb-16">
        <h1 class="text-4xl lg:text-5xl font-bold mb-4">
          <span style="background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899); background-clip: text; -webkit-background-clip: text; color: transparent;">
            GitHub 每周热门项目
          </span>
        </h1>
        <p class="text-slate-400 text-lg max-w-2xl mx-auto">
          探索 GitHub 上最新、最热门的开源项目趋势
        </p>
      </header>

      <!-- 数据可视化图表 -->
      <section class="mb-16">
        <StatsChart :stats="stats" />
      </section>

      <!-- 报告列表 -->
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
                重试
              </button>
              <button @click="checkConnection" class="btn-secondary">
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
          >
            <div class="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-bl from-blue-500/10 to-transparent rounded-full transform translate-x-8 -translate-y-8"></div>
            
            <div v-if="index === 0" class="absolute top-4 right-4 z-10">
              <div class="bg-gradient-to-r from-pink-500 to-rose-500 text-white text-xs px-3 py-1 rounded-full shadow-lg animate-pulse">
                <i class="fa fa-star mr-1"></i>最新
              </div>
            </div>
            
            <div class="relative p-6">
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
            
            <div class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 opacity-60 group-hover:opacity-100 transition-opacity duration-300"></div>
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
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import * as reportApi from '../api/reports'
import type { Report, Stats } from '../api/reports'
import ReportModal from '../components/ReportModal.vue'
import StatsChart from '../components/StatsChart.vue'

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
const sortOrder = ref('desc')
const displayLimit = ref(12)
const connectionStatus = ref(false)
const lastUpdate = ref<Date | null>(null)

// 计算属性
const filteredReports = computed(() => {
  let filtered = reports.value
  
  if (searchFilter.value.trim()) {
    const searchTerm = searchFilter.value.trim().toLowerCase()
    filtered = filtered.filter(report => 
      report.date.toLowerCase().includes(searchTerm) ||
      report.project_count.toString().includes(searchTerm)
    )
  }
  
  if (sortOrder.value === 'asc') {
    filtered = [...filtered].sort((a, b) => a.date.localeCompare(b.date))
  } else if (sortOrder.value === 'desc') {
    filtered = [...filtered].sort((a, b) => b.date.localeCompare(a.date))
  } else if (sortOrder.value === 'projects') {
    filtered = [...filtered].sort((a, b) => b.project_count - a.project_count)
  }
  
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

// 健康检查
let healthCheckInterval: NodeJS.Timeout | null = null

function startHealthCheck() {
  checkConnection()
  healthCheckInterval = setInterval(checkConnection, 30000)
}

function stopHealthCheck() {
  if (healthCheckInterval) {
    clearInterval(healthCheckInterval)
    healthCheckInterval = null
  }
}

async function checkConnection() {
  try {
    connectionStatus.value = await reportApi.healthCheck()
  } catch {
    connectionStatus.value = false
  }
}

// 数据获取
async function initializeApp() {
  console.log(`🌐 连接到 API: ${reportApi.getApiBaseUrl()}`)
  await Promise.all([
    fetchReports(),
    fetchStats()
  ])
}

async function refreshData() {
  await initializeApp()
}

async function fetchReports() {
  try {
    loading.value = true
    error.value = null
    reports.value = await reportApi.getReports()
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
    stats.value = await reportApi.getStats()
    console.log('📊 统计数据更新成功')
  } catch (err: any) {
    console.error('获取统计数据失败:', err)
  }
}

// 用户交互
async function openReport(date: string) {
  try {
    selectedReport.value = await reportApi.getReportContent(date)
    console.log(`📄 打开报告: ${date}`)
  } catch (err) {
    console.error(`获取报告 ${date} 内容失败:`, err)
    error.value = `获取报告 ${date} 内容失败`
  }
}

function closeReport() {
  selectedReport.value = null
}

function viewProjects(date: string) {
  router.push(`/projects/${date}`)
}

function handleSearch() {
  // 计算属性会自动响应
}

function clearSearch() {
  searchFilter.value = ''
}

// 格式化函数
function formatDateShort(dateStr: string): string {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric', weekday: 'short' })
}

function formatDay(dateStr: string): string {
  return new Date(dateStr).getDate().toString()
}

function formatDateWeek(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString('zh-CN', { weekday: 'long' })
}
</script>
