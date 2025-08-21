<template>
  <div class="bg-gradient-to-br from-slate-800 to-slate-900 text-slate-100 min-h-screen font-sans">
    <!-- 粒子背景效果 -->
    <div class="fixed inset-0 -z-10 overflow-hidden">
      <div class="absolute top-[10%] left-[20%] w-64 h-64 bg-blue-500/20 rounded-full filter blur-3xl animate-pulse-slow"></div>
      <div class="absolute top-[60%] right-[15%] w-80 h-80 bg-purple-500/20 rounded-full filter blur-3xl animate-pulse-slow delay-1000"></div>
      <div class="absolute bottom-[10%] left-[30%] w-72 h-72 bg-pink-500/20 rounded-full filter blur-3xl animate-pulse-slow delay-2000"></div>
    </div>

    <!-- 顶部导航栏 -->
    <header class="glass-effect sticky top-0 z-50 border-b border-white/10">
      <div class="container mx-auto px-4 py-5 flex flex-col md:flex-row justify-between items-center">
        <div class="flex items-center space-x-3 mb-4 md:mb-0">
          <div class="bg-gradient-to-br from-blue-500 to-purple-600 p-2 rounded-lg shadow-lg">
            <i class="fa fa-github text-white text-2xl"></i>
          </div>
          <h1 class="text-[clamp(1.5rem,3vw,2.2rem)] font-bold">
            <span class="text-gradient bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent">
              GitHub每周热门项目
            </span>
          </h1>
        </div>
        <div class="flex items-center space-x-6">
          <router-link to="/about" class="text-slate-300 hover:text-white transition-colors font-medium">
            关于项目
          </router-link>
          <div class="relative group">
            <button class="bg-gradient-to-r from-blue-500 to-purple-600 px-5 py-2 rounded-lg font-medium transition-all shadow-lg hover:shadow-blue-500/30 flex items-center cursor-pointer">
              <i class="fa fa-weixin mr-2"></i>扫码关注
            </button>
            <div class="absolute hidden group-hover:block right-0 w-40 bg-white p-2 rounded-lg shadow-xl z-50 top-full mt-2">
              <div class="w-full h-32 bg-slate-200 rounded flex items-center justify-center text-slate-600">
                二维码
              </div>
              <p class="text-center text-sm text-gray-800 mt-1">扫码关注</p>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="container mx-auto px-4 py-12">
      <!-- 页面标题和统计 -->
      <section class="mb-12 text-center">
        <h2 class="text-[clamp(1.8rem,4vw,3rem)] font-bold mb-4">每日热门项目报告</h2>
        <p class="text-slate-400 max-w-2xl mx-auto mb-8 text-lg">
          探索 GitHub 每日热门开源项目，点击日期卡片查看详细分析报告
        </p>
        
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-3xl mx-auto">
          <div class="bg-slate-800/50 rounded-xl p-4 card-border hover-lift backdrop-blur-sm">
            <div class="text-slate-400 text-sm mb-1">总报告数</div>
            <div class="text-2xl font-bold text-white">{{ stats.totalReports }}</div>
          </div>
          <div class="bg-slate-800/50 rounded-xl p-4 card-border hover-lift backdrop-blur-sm">
            <div class="text-slate-400 text-sm mb-1">总项目数</div>
            <div class="text-2xl font-bold text-white">{{ stats.totalProjects }}</div>
          </div>
          <div class="bg-slate-800/50 rounded-xl p-4 card-border hover-lift backdrop-blur-sm">
            <div class="text-slate-400 text-sm mb-1">热门语言</div>
            <div class="text-2xl font-bold text-white">{{ stats.topLanguage }}</div>
          </div>
          <div class="bg-slate-800/50 rounded-xl p-4 card-border hover-lift backdrop-blur-sm">
            <div class="text-slate-400 text-sm mb-1">本周新增</div>
            <div class="text-2xl font-bold text-white">{{ stats.weeklyNew }}</div>
          </div>
        </div>
      </section>

      <!-- 日期卡片网格 -->
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
        <div v-else-if="error" class="col-span-full text-center text-red-400 py-16">
          <i class="fa fa-exclamation-triangle text-5xl mb-4"></i>
          <p>{{ error }}</p>
          <button @click="fetchReports" class="mt-4 bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-colors">
            重试
          </button>
        </div>
        
        <!-- 报告卡片网格 -->
        <div v-else-if="filteredReports.length === 0" class="col-span-full py-16 text-center">
          <i class="fa fa-calendar-o text-5xl text-slate-600 mb-4"></i>
          <p class="text-slate-400">未找到报告</p>
        </div>
        
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <div 
            v-for="(report, index) in filteredReports" 
            :key="report.date"
            @click="openReport(report.date)"
            class="date-card bg-slate-800/50 rounded-2xl overflow-hidden card-border hover-lift cursor-pointer animate-fadeInUp backdrop-blur-sm"
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
import { ref, onMounted, computed } from 'vue'
import { getReports, getReportByDate, getStats, type Report, type Stats } from '../api/reports'
import ReportModal from '../components/ReportModal.vue'

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

// 计算属性
const latestDate = computed(() => {
  if (reports.value.length === 0) return '暂无'
  const latest = reports.value[0].date
  return formatDate(latest)
})

const filteredReports = computed(() => {
  if (!searchFilter.value.trim()) return reports.value
  return reports.value.filter(report => 
    report.date.includes(searchFilter.value.trim())
  )
})

// 生命周期钩子
onMounted(async () => {
  await fetchReports()
  await fetchStats()
})

// 方法
async function fetchReports() {
  try {
    loading.value = true
    error.value = null
    reports.value = await getReports()
  } catch (err) {
    error.value = '获取报告列表失败'
    console.error('Error fetching reports:', err)
  } finally {
    loading.value = false
  }
}

async function fetchStats() {
  try {
    stats.value = await getStats()
  } catch (err) {
    console.error('Error fetching stats:', err)
  }
}

async function openReport(date: string) {
  try {
    const report = await getReportByDate(date)
    selectedReport.value = report
  } catch (err) {
    error.value = '获取报告详情失败'
    console.error('Error fetching report:', err)
  }
}

function closeReport() {
  selectedReport.value = null
}

function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
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

function formatTime(dateStr: string): string {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    month: '2-digit',
    day: '2-digit'
  })
}
</script>