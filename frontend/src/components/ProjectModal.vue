<template>
  <transition name="modal">
    <div 
      v-if="visible" 
      class="fixed inset-0 bg-black/70 z-50 flex items-center justify-center p-4"
      @click="handleBackdropClick"
    >
      <div 
        ref="modalContent"
        class="bg-slate-800 rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-hidden flex flex-col animate-fadeIn"
        @click.stop
      >
        <!-- 模态框头部 -->
        <div class="p-6 border-b border-white/10 flex justify-between items-center">
          <div class="flex items-center flex-1 min-w-0">
            <i class="fa fa-github text-primary mr-3 text-xl"></i>
            <div class="min-w-0 flex-1">
              <h3 class="text-xl font-bold text-white truncate">{{ projectName }}</h3>
              <p class="text-slate-400 text-sm truncate">{{ project?.url }}</p>
            </div>
          </div>
          <button 
            @click="$emit('close')" 
            class="p-2 rounded-full hover:bg-white/10 transition-colors flex-shrink-0 ml-4"
          >
            <i class="fa fa-times text-xl text-slate-400"></i>
          </button>
        </div>

        <!-- 模态框内容 -->
        <div class="flex-grow overflow-y-auto">
          <div v-if="loading" class="h-full flex flex-col items-center justify-center py-12">
            <div class="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin mb-4"></div>
            <p class="text-slate-400">加载项目详情中...</p>
          </div>

          <div v-else-if="project" class="p-6">
            <!-- 项目描述 -->
            <div class="mb-6">
              <h4 class="text-lg font-semibold text-white mb-3 flex items-center">
                <i class="fa fa-info-circle text-primary mr-2"></i>
                项目描述
              </h4>
              <p class="text-slate-300 leading-relaxed bg-slate-900/50 p-4 rounded-lg">
                {{ project.description || '暂无描述' }}
              </p>
            </div>

            <!-- 技术信息 -->
            <div class="mb-6">
              <h4 class="text-lg font-semibold text-white mb-3 flex items-center">
                <i class="fa fa-code text-primary mr-2"></i>
                技术信息
              </h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="tech-info-item">
                  <span class="label">主要语言</span>
                  <span 
                    class="value language-tag"
                    :class="getLanguageClass(project.language)"
                  >
                    {{ project.language || '未知' }}
                  </span>
                </div>
                <div class="tech-info-item">
                  <span class="label">创建时间</span>
                  <span class="value">{{ formatFullDate(project.created_at) }}</span>
                </div>
                <div class="tech-info-item">
                  <span class="label">最后更新</span>
                  <span class="value">{{ formatFullDate(project.updated_at) }}</span>
                </div>
                <div class="tech-info-item">
                  <span class="label">开放问题</span>
                  <span class="value">{{ formatNumber(project.open_issues) }}</span>
                </div>
              </div>
            </div>

            <!-- 统计数据 -->
            <div class="mb-6">
              <h4 class="text-lg font-semibold text-white mb-3 flex items-center">
                <i class="fa fa-bar-chart text-primary mr-2"></i>
                项目统计
              </h4>
              <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="stat-card">
                  <div class="stat-icon bg-yellow-500/20">
                    <i class="fa fa-star text-yellow-400"></i>
                  </div>
                  <div class="stat-content">
                    <div class="stat-value">{{ formatNumber(project.stars) }}</div>
                    <div class="stat-label">Stars</div>
                  </div>
                </div>
                <div class="stat-card">
                  <div class="stat-icon bg-blue-500/20">
                    <i class="fa fa-code-fork text-blue-400"></i>
                  </div>
                  <div class="stat-content">
                    <div class="stat-value">{{ formatNumber(project.forks) }}</div>
                    <div class="stat-label">Forks</div>
                  </div>
                </div>
                <div class="stat-card">
                  <div class="stat-icon bg-green-500/20">
                    <i class="fa fa-users text-green-400"></i>
                  </div>
                  <div class="stat-content">
                    <div class="stat-value">{{ formatNumber(project.contributor_count) }}</div>
                    <div class="stat-label">贡献者</div>
                  </div>
                </div>
                <div class="stat-card">
                  <div class="stat-icon bg-purple-500/20">
                    <i class="fa fa-eye text-purple-400"></i>
                  </div>
                  <div class="stat-content">
                    <div class="stat-value">{{ formatNumber(project.watchers) }}</div>
                    <div class="stat-label">关注者</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="h-full flex flex-col items-center justify-center py-12">
            <i class="fa fa-exclamation-triangle text-red-400 text-4xl mb-4"></i>
            <p class="text-slate-400">加载项目详情失败</p>
          </div>
        </div>

        <!-- 模态框底部 -->
        <div class="p-6 border-t border-white/10 flex justify-between items-center">
          <div class="text-slate-400 text-sm">
            分析时间：{{ project?.summary_date ? formatFullDate(project.summary_date) : '未知' }}
          </div>
          <div class="flex space-x-3">
            <a 
              v-if="project?.url" 
              :href="project.url" 
              target="_blank" 
              rel="noopener noreferrer"
              class="px-4 py-2 bg-primary rounded-lg hover:bg-primary/80 transition-colors flex items-center"
            >
              <i class="fa fa-external-link mr-2"></i>
              访问项目
            </a>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type { Project } from '@/api/reports'
import { getProjectDetails } from '@/api/reports'

interface Props {
  visible: boolean
  projectName?: string
}

const props = defineProps<Props>()

const emit = defineEmits<{
  close: []
}>()

const modalContent = ref<HTMLElement>()
const loading = ref(false)
const project = ref<Project | null>(null)

const projectDisplayName = computed(() => {
  if (!props.projectName) return ''
  const parts = props.projectName.split('/')
  return parts.length > 1 ? parts[1] : props.projectName
})

watch(() => props.visible, async (visible) => {
  if (visible && props.projectName) {
    await loadProjectDetails()
  }
})

const loadProjectDetails = async () => {
  if (!props.projectName) return
  
  loading.value = true
  try {
    project.value = await getProjectDetails(props.projectName)
  } catch (error) {
    console.error('Failed to load project details:', error)
    project.value = null
  } finally {
    loading.value = false
  }
}

const handleBackdropClick = (event: MouseEvent) => {
  if (event.target === event.currentTarget) {
    emit('close')
  }
}

const formatNumber = (num: number | string): string => {
  if (typeof num === 'string') return num
  if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`
  if (num >= 1000) return `${(num / 1000).toFixed(1)}K`
  return num.toString()
}

const formatFullDate = (dateStr: string): string => {
  if (!dateStr || dateStr === 'N/A') return '未知'
  try {
    const date = new Date(dateStr)
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  } catch {
    return '未知'
  }
}

const getLanguageClass = (language: string): string => {
  const languageColors: Record<string, string> = {
    'JavaScript': 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30',
    'TypeScript': 'bg-blue-500/20 text-blue-400 border border-blue-500/30',
    'Python': 'bg-green-500/20 text-green-400 border border-green-500/30',
    'Java': 'bg-orange-500/20 text-orange-400 border border-orange-500/30',
    'Go': 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30',
    'Rust': 'bg-red-500/20 text-red-400 border border-red-500/30',
    'C++': 'bg-purple-500/20 text-purple-400 border border-purple-500/30',
    'C': 'bg-gray-500/20 text-gray-400 border border-gray-500/30',
    'PHP': 'bg-indigo-500/20 text-indigo-400 border border-indigo-500/30',
    'Ruby': 'bg-red-600/20 text-red-400 border border-red-600/30',
    'Swift': 'bg-orange-600/20 text-orange-400 border border-orange-600/30',
    'Kotlin': 'bg-purple-600/20 text-purple-400 border border-purple-600/30'
  }
  
  return languageColors[language] || 'bg-slate-500/20 text-slate-400 border border-slate-500/30'
}
</script>

<style scoped>
.modal-enter-active, .modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from, .modal-leave-to {
  opacity: 0;
}

.tech-info-item {
  @apply bg-slate-900/50 p-3 rounded-lg flex justify-between items-center;
}

.tech-info-item .label {
  @apply text-slate-400 text-sm;
}

.tech-info-item .value {
  @apply text-white font-medium;
}

.language-tag {
  @apply px-2 py-1 rounded-full text-xs font-medium;
}

.stat-card {
  @apply bg-slate-900/50 p-4 rounded-lg flex items-center space-x-3 hover:bg-slate-900/70 transition-colors;
}

.stat-icon {
  @apply w-10 h-10 rounded-lg flex items-center justify-center;
}

.stat-content {
  @apply flex-1;
}

.stat-value {
  @apply text-lg font-bold text-white;
}

.stat-label {
  @apply text-slate-400 text-xs;
}
</style>
