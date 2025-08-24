<template>
  <div class="bg-gradient-to-br from-slate-800 to-slate-900 text-slate-100 min-h-screen font-sans">
    <!-- 粒子背景效果 -->
    <div class="fixed inset-0 -z-10 overflow-hidden">
      <div class="absolute top-[10%] left-[20%] w-64 h-64 bg-blue-500/20 rounded-full filter blur-3xl animate-pulse-slow"></div>
      <div class="absolute top-[60%] right-[15%] w-80 h-80 bg-purple-500/20 rounded-full filter blur-3xl animate-pulse-slow delay-1000"></div>
      <div class="absolute bottom-[10%] left-[30%] w-72 h-72 bg-pink-500/20 rounded-full filter blur-3xl animate-pulse-slow delay-2000"></div>
    </div>

    <!-- 顶部导航栏 -->
    <header class="glass-effect sticky top-0 z-40 border-b border-white/10">
      <div class="container mx-auto px-4 py-5 flex justify-between items-center">
        <div class="flex items-center space-x-3">
          <button 
            @click="$router.go(-1)"
            class="p-2 rounded-lg hover:bg-white/10 transition-colors"
          >
            <i class="fa fa-arrow-left text-xl"></i>
          </button>
          <div class="bg-gradient-to-br from-blue-500 to-purple-600 p-2 rounded-lg shadow-lg">
            <i class="fa fa-calendar text-white text-xl"></i>
          </div>
          <div>
            <h1 style="background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899); background-clip: text; -webkit-background-clip: text; color: transparent;" class="text-xl font-bold">
              {{ displayDate }} 热门项目
            </h1>
            <p class="text-slate-400 text-sm">{{ projectCount }} 个项目</p>
          </div>
        </div>
        
        <!-- 筛选和排序 -->
        <div class="flex items-center space-x-4">
          <div class="relative">
            <select 
              v-model="sortBy" 
              class="bg-slate-800/50 border border-white/10 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option value="stars">按 Stars 排序</option>
              <option value="forks">按 Forks 排序</option>
              <option value="contributors">按贡献者排序</option>
              <option value="name">按名称排序</option>
            </select>
          </div>
          <div class="relative">
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="搜索项目..." 
              class="bg-slate-800/50 border border-white/10 rounded-lg px-4 py-2 pl-10 text-sm focus:outline-none focus:ring-2 focus:ring-primary w-64"
            >
            <i class="fa fa-search absolute left-3 top-3 text-slate-400"></i>
          </div>
        </div>
      </div>
    </header>

    <!-- 主内容 -->
    <main class="container mx-auto px-4 py-8">
      <!-- 加载状态 -->
      <div v-if="loading" class="flex justify-center items-center py-20">
        <div class="text-center">
          <div class="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin mb-4 mx-auto"></div>
          <p class="text-slate-400">加载项目列表中...</p>
        </div>
      </div>

      <!-- 错误状态 -->
      <div v-else-if="error" class="flex justify-center items-center py-20">
        <div class="text-center">
          <i class="fa fa-exclamation-triangle text-red-400 text-4xl mb-4"></i>
          <p class="text-slate-400 mb-4">{{ error }}</p>
          <button 
            @click="loadProjects" 
            class="px-4 py-2 bg-primary rounded-lg hover:bg-primary/80 transition-colors"
          >
            重试
          </button>
        </div>
      </div>

      <!-- 项目网格 -->
      <div v-else-if="filteredProjects.length > 0">
        <!-- 统计信息 -->
        <div class="mb-8 grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="bg-slate-800/50 rounded-xl p-4 card-border">
            <div class="text-slate-400 text-sm mb-1">项目总数</div>
            <div class="text-2xl font-bold text-white">{{ projectCount }}</div>
          </div>
          <div class="bg-slate-800/50 rounded-xl p-4 card-border">
            <div class="text-slate-400 text-sm mb-1">平均 Stars</div>
            <div class="text-2xl font-bold text-white">{{ averageStars }}</div>
          </div>
          <div class="bg-slate-800/50 rounded-xl p-4 card-border">
            <div class="text-slate-400 text-sm mb-1">最多语言</div>
            <div class="text-2xl font-bold text-white">{{ topLanguage }}</div>
          </div>
          <div class="bg-slate-800/50 rounded-xl p-4 card-border">
            <div class="text-slate-400 text-sm mb-1">总 Forks</div>
            <div class="text-2xl font-bold text-white">{{ totalForks }}</div>
          </div>
        </div>

        <!-- 项目卡片网格 -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <ProjectCard
            v-for="(project, index) in filteredProjects"
            :key="project.name"
            :project="project"
            :index="index"
            @click="handleProjectClick"
          />
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else class="flex justify-center items-center py-20">
        <div class="text-center">
          <i class="fa fa-inbox text-slate-600 text-4xl mb-4"></i>
          <p class="text-slate-400">未找到项目</p>
        </div>
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
import { useRoute } from 'vue-router'
import ProjectCard from '@/components/ProjectCard.vue'
import ProjectModal from '@/components/ProjectModal.vue'
import { getProjectsByDate, type Project } from '@/api/reports'

const route = useRoute()

const loading = ref(false)
const error = ref('')
const projects = ref<Project[]>([])
const searchQuery = ref('')
const sortBy = ref('stars')
const showProjectModal = ref(false)
const selectedProjectName = ref('')

const date = computed(() => route.params.date as string)

const displayDate = computed(() => {
  try {
    const dateObj = new Date(date.value)
    return dateObj.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      weekday: 'long'
    })
  } catch {
    return date.value
  }
})

const filteredProjects = computed(() => {
  let result = [...projects.value]

  // 搜索过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(project => 
      project.name.toLowerCase().includes(query) ||
      project.description.toLowerCase().includes(query) ||
      project.language.toLowerCase().includes(query)
    )
  }

  // 排序
  result.sort((a, b) => {
    switch (sortBy.value) {
      case 'stars':
        return Number(b.stars) - Number(a.stars)
      case 'forks':
        return Number(b.forks) - Number(a.forks)
      case 'contributors':
        return Number(b.contributor_count) - Number(a.contributor_count)
      case 'name':
        return a.name.localeCompare(b.name)
      default:
        return 0
    }
  })

  return result
})

const projectCount = computed(() => projects.value.length)

const averageStars = computed(() => {
  if (projects.value.length === 0) return '0'
  const total = projects.value.reduce((sum, project) => sum + Number(project.stars), 0)
  const avg = total / projects.value.length
  return avg >= 1000 ? `${(avg / 1000).toFixed(1)}K` : Math.round(avg).toString()
})

const topLanguage = computed(() => {
  const languageCount = projects.value.reduce((acc, project) => {
    if (project.language && project.language !== 'N/A') {
      acc[project.language] = (acc[project.language] || 0) + 1
    }
    return acc
  }, {} as Record<string, number>)

  const sortedLanguages = Object.entries(languageCount).sort(([,a], [,b]) => b - a)
  return sortedLanguages[0]?.[0] || 'N/A'
})

const totalForks = computed(() => {
  const total = projects.value.reduce((sum, project) => sum + Number(project.forks), 0)
  return total >= 1000 ? `${(total / 1000).toFixed(1)}K` : total.toString()
})

const loadProjects = async () => {
  if (!date.value) return

  loading.value = true
  error.value = ''

  try {
    projects.value = await getProjectsByDate(date.value)
  } catch (err) {
    error.value = '加载项目列表失败'
    console.error('Failed to load projects:', err)
  } finally {
    loading.value = false
  }
}

const handleProjectClick = (project: Project) => {
  selectedProjectName.value = project.name
  showProjectModal.value = true
}

// 监听路由变化
watch(() => route.params.date, loadProjects, { immediate: true })

onMounted(() => {
  loadProjects()
})
</script>

<style scoped>
.text-gradient {
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
  background-image: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899);
}
</style>