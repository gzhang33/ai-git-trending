<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
    <!-- 顶部导航栏 -->
    <header class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center">
            <div class="flex-shrink-0 flex items-center">
              <div class="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <i class="fa fa-github text-white text-lg"></i>
              </div>
              <h1 class="ml-3 text-xl font-bold text-gray-900">
                GitHub热门项目 - 传递最新开源解决方案
              </h1>
            </div>
          </div>
          
          <nav class="hidden md:flex items-center space-x-8">
            <a href="#" class="text-gray-600 hover:text-gray-900 font-medium transition-colors">AI方案库</a>
            <a href="#" class="text-gray-600 hover:text-gray-900 font-medium transition-colors">AI日报</a>
            <a href="#" class="text-gray-600 hover:text-gray-900 font-medium transition-colors">AI产品</a>
            <a href="#" class="text-gray-600 hover:text-gray-900 font-medium transition-colors">分类方案</a>
            <a href="#" class="text-gray-600 hover:text-gray-900 font-medium transition-colors">关于我们</a>
          </nav>
          
          <div class="flex items-center space-x-4">
            <button class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
              提交项目
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- 搜索栏 -->
      <div class="mb-8">
        <div class="relative max-w-2xl mx-auto">
          <input 
            v-model="searchQuery"
            type="text" 
            placeholder="搜索GitHub热门项目..."
            class="w-full px-6 py-4 text-lg border-2 border-gray-200 rounded-2xl focus:outline-none focus:border-blue-500 transition-colors pl-14"
          >
          <i class="fa fa-search absolute left-5 top-1/2 transform -translate-y-1/2 text-gray-400 text-lg"></i>
        </div>
      </div>

      <!-- 筛选选项 -->
      <div class="mb-8 flex flex-wrap gap-4 justify-center">
        <button 
          v-for="category in categories" 
          :key="category"
          @click="selectedCategory = category"
          :class="[
            'px-6 py-2 rounded-full text-sm font-medium transition-all',
            selectedCategory === category 
              ? 'bg-blue-600 text-white shadow-lg' 
              : 'bg-white text-gray-600 hover:bg-gray-50 border border-gray-200'
          ]"
        >
          {{ category }}
        </button>
      </div>

      <!-- 统计信息 -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-6 mb-12">
        <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <div class="text-sm text-gray-500 mb-2">项目总数</div>
          <div class="text-3xl font-bold text-gray-900">{{ totalProjects }}</div>
        </div>
        <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <div class="text-sm text-gray-500 mb-2">今日新增</div>
          <div class="text-3xl font-bold text-blue-600">{{ todayNew }}</div>
        </div>
        <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <div class="text-sm text-gray-500 mb-2">热门语言</div>
          <div class="text-lg font-bold text-gray-900">{{ topLanguage }}</div>
        </div>
        <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <div class="text-sm text-gray-500 mb-2">总分叉数</div>
          <div class="text-lg font-bold text-gray-900">{{ totalForks }}</div>
        </div>
      </div>

      <!-- 项目卡片网格 -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <div 
          v-for="(project, index) in filteredProjects" 
          :key="project.name"
          @click="viewProjectDetails(project)"
          class="bg-white rounded-2xl overflow-hidden shadow-sm border border-gray-100 hover:shadow-xl hover:-translate-y-2 transition-all duration-300 cursor-pointer group"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <!-- 项目预览图 -->
          <div class="aspect-video bg-gradient-to-br from-blue-50 to-purple-50 relative overflow-hidden">
            <div class="absolute inset-0 bg-gradient-to-br from-blue-500/10 to-purple-500/10 flex items-center justify-center">
              <div class="text-center">
                <i class="fa fa-github text-4xl text-gray-400 mb-2"></i>
                <div class="text-sm text-gray-500 font-medium">{{ project.language || 'Unknown' }}</div>
              </div>
            </div>
            
            <!-- 悬停时显示的操作按钮 -->
            <div class="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity">
              <button 
                @click.stop="openProjectUrl(project.url)"
                class="bg-white/90 hover:bg-white p-2 rounded-lg shadow-md transition-colors"
              >
                <i class="fa fa-external-link text-gray-600"></i>
              </button>
            </div>
            
            <!-- 项目星标数 -->
            <div class="absolute bottom-4 left-4">
              <div class="bg-white/90 px-3 py-1 rounded-full text-sm font-medium text-gray-700 flex items-center">
                <i class="fa fa-star text-yellow-500 mr-1"></i>
                {{ formatNumber(project.stars) }}
              </div>
            </div>
          </div>
          
          <!-- 项目信息 -->
          <div class="p-6">
            <div class="mb-3">
              <h3 class="font-bold text-gray-900 text-lg mb-2 line-clamp-1">
                {{ getProjectDisplayName(project.name) }}
              </h3>
              <p class="text-gray-600 text-sm line-clamp-3 leading-relaxed">
                {{ project.description || '暂无描述' }}
              </p>
            </div>
            
            <!-- 项目标签 -->
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <span 
                  v-if="project.language"
                  class="px-2 py-1 text-xs rounded-full font-medium"
                  :class="getLanguageStyle(project.language)"
                >
                  {{ project.language }}
                </span>
              </div>
              
              <div class="flex items-center text-sm text-gray-500">
                <i class="fa fa-code-fork mr-1"></i>
                {{ formatNumber(project.forks) }}
              </div>
            </div>
            
            <!-- 更新时间 -->
            <div class="mt-4 pt-4 border-t border-gray-100">
              <div class="text-xs text-gray-500">
                更新于 {{ formatDate(project.updated_at) }}
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 加载更多 -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-flex items-center px-6 py-3 bg-white rounded-xl shadow-sm border border-gray-100">
          <div class="animate-spin rounded-full h-5 w-5 border-2 border-blue-600 border-t-transparent mr-3"></div>
          <span class="text-gray-600">加载中...</span>
        </div>
      </div>
      
      <!-- 空状态 -->
      <div v-else-if="filteredProjects.length === 0" class="text-center py-20">
        <i class="fa fa-search text-6xl text-gray-300 mb-4"></i>
        <h3 class="text-xl font-semibold text-gray-500 mb-2">未找到相关项目</h3>
        <p class="text-gray-400">尝试调整搜索关键词或筛选条件</p>
      </div>
      
      <!-- 加载更多按钮 -->
      <div v-if="!loading && filteredProjects.length > 0 && hasMore" class="text-center pt-12">
        <button 
          @click="loadMore"
          class="px-8 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors"
        >
          加载更多
        </button>
      </div>
    </main>

    <!-- 项目详情模态框 -->
    <ProjectModal
      :visible="showProjectModal"
      :project-name="selectedProjectName"
      @close="showProjectModal = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { getProjectsByDate, reportApi, type Project } from '@/api/reports'
import ProjectModal from '@/components/ProjectModal.vue'

// 响应式数据
const projects = ref<Project[]>([])
const loading = ref(false)
const searchQuery = ref('')
const selectedCategory = ref('全部')
const showProjectModal = ref(false)
const selectedProjectName = ref('')
const page = ref(1)
const pageSize = ref(20)
const hasMore = ref(true)

// 分类选项
const categories = ref([
  '全部', 'AI/机器学习', 'Web开发', '移动开发', '数据科学', 
  '区块链', '游戏开发', 'DevOps', '系统工具', '其他'
])

// 统计数据
const totalProjects = ref(0)
const todayNew = ref(0)
const topLanguage = ref('JavaScript')
const totalForks = ref('0')

// 计算属性
const filteredProjects = computed(() => {
  let filtered = projects.value

  // 搜索过滤
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(project => 
      project.name.toLowerCase().includes(query) ||
      project.description.toLowerCase().includes(query) ||
      (project.language && project.language.toLowerCase().includes(query))
    )
  }

  // 分类过滤
  if (selectedCategory.value !== '全部') {
    filtered = filtered.filter(project => {
      const category = getProjectCategory(project)
      return category === selectedCategory.value
    })
  }

  return filtered
})

// 生命周期钩子
onMounted(async () => {
  await loadProjects()
  await loadStats()
})

// 监听搜索和分类变化
watch([searchQuery, selectedCategory], () => {
  // 重置分页
  page.value = 1
  hasMore.value = true
})

// 方法
async function loadProjects() {
  try {
    loading.value = true
    // 获取最新日期的项目数据
    const reports = await reportApi.getReports()
    if (reports.length > 0) {
      const latestDate = reports[0].date
      const projectData = await getProjectsByDate(latestDate)
      projects.value = projectData
    }
  } catch (error) {
    console.error('加载项目数据失败:', error)
  } finally {
    loading.value = false
  }
}

async function loadStats() {
  try {
    const stats = await reportApi.getStats()
    totalProjects.value = stats.totalProjects
    todayNew.value = stats.weeklyNew
    topLanguage.value = stats.topLanguage
    totalForks.value = stats.totalForks
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

function loadMore() {
  page.value += 1
  // 这里可以实现分页加载逻辑
}

function viewProjectDetails(project: Project) {
  selectedProjectName.value = project.name
  showProjectModal.value = true
}

function openProjectUrl(url: string) {
  window.open(url, '_blank')
}

// 工具函数
function getProjectDisplayName(name: string): string {
  const parts = name.split('/')
  return parts.length > 1 ? parts[1] : name
}

function getProjectCategory(project: Project): string {
  const name = project.name.toLowerCase()
  const desc = project.description.toLowerCase()
  const lang = project.language?.toLowerCase() || ''

  if (name.includes('ai') || name.includes('ml') || desc.includes('machine learning') || desc.includes('artificial intelligence')) {
    return 'AI/机器学习'
  }
  if (lang.includes('javascript') || lang.includes('typescript') || desc.includes('web') || desc.includes('react') || desc.includes('vue')) {
    return 'Web开发'
  }
  if (lang.includes('swift') || lang.includes('kotlin') || desc.includes('mobile') || desc.includes('android') || desc.includes('ios')) {
    return '移动开发'
  }
  if (desc.includes('data') || desc.includes('analytics') || lang.includes('r') || lang.includes('python')) {
    return '数据科学'
  }
  if (desc.includes('blockchain') || desc.includes('crypto') || desc.includes('bitcoin')) {
    return '区块链'
  }
  if (desc.includes('game') || desc.includes('unity') || desc.includes('gamedev')) {
    return '游戏开发'
  }
  if (desc.includes('devops') || desc.includes('docker') || desc.includes('kubernetes') || desc.includes('ci/cd')) {
    return 'DevOps'
  }
  if (desc.includes('tool') || desc.includes('utility') || desc.includes('cli')) {
    return '系统工具'
  }
  
  return '其他'
}

function formatNumber(num: number | string): string {
  if (typeof num === 'string') return num
  if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`
  if (num >= 1000) return `${(num / 1000).toFixed(1)}K`
  return num.toString()
}

function formatDate(dateStr: string): string {
  if (!dateStr || dateStr === 'N/A') return '未知'
  try {
    const date = new Date(dateStr)
    const now = new Date()
    const diffTime = Math.abs(now.getTime() - date.getTime())
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    
    if (diffDays === 0) return '今天'
    if (diffDays === 1) return '昨天'
    if (diffDays < 7) return `${diffDays}天前`
    if (diffDays < 30) return `${Math.floor(diffDays / 7)}周前`
    if (diffDays < 365) return `${Math.floor(diffDays / 30)}个月前`
    return `${Math.floor(diffDays / 365)}年前`
  } catch {
    return '未知'
  }
}

function getLanguageStyle(language: string): string {
  const languageColors: Record<string, string> = {
    'JavaScript': 'bg-yellow-100 text-yellow-800 border border-yellow-200',
    'TypeScript': 'bg-blue-100 text-blue-800 border border-blue-200',
    'Python': 'bg-green-100 text-green-800 border border-green-200',
    'Java': 'bg-orange-100 text-orange-800 border border-orange-200',
    'Go': 'bg-cyan-100 text-cyan-800 border border-cyan-200',
    'Rust': 'bg-red-100 text-red-800 border border-red-200',
    'C++': 'bg-purple-100 text-purple-800 border border-purple-200',
    'C': 'bg-gray-100 text-gray-800 border border-gray-200',
    'PHP': 'bg-indigo-100 text-indigo-800 border border-indigo-200',
    'Ruby': 'bg-pink-100 text-pink-800 border border-pink-200',
    'Swift': 'bg-orange-100 text-orange-800 border border-orange-200',
    'Kotlin': 'bg-purple-100 text-purple-800 border border-purple-200'
  }
  
  return languageColors[language] || 'bg-gray-100 text-gray-800 border border-gray-200'
}
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.group:hover .group-hover\:opacity-100 {
  opacity: 1;
}
</style>