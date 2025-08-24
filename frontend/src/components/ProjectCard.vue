<template>
  <div 
    class="project-card bg-slate-800/50 rounded-2xl overflow-hidden card-border hover-lift cursor-pointer animate-fadeInUp group"
    @click="$emit('click', project)"
    :style="{ animationDelay: `${index * 0.1}s` }"
  >
    <!-- 项目头部 -->
    <div class="p-6">
      <div class="flex justify-between items-start mb-4">
        <div class="flex-1 min-w-0">
          <div class="flex items-center mb-2">
            <i class="fa fa-github text-primary mr-2"></i>
            <h3 class="text-lg font-bold text-white truncate">{{ projectName }}</h3>
          </div>
          <p class="text-slate-400 text-sm mb-3 line-clamp-2 leading-relaxed">
            {{ project.description || '暂无描述' }}
          </p>
        </div>
        <div class="ml-4 flex-shrink-0">
          <span 
            v-if="project.language" 
            class="language-tag px-2 py-1 rounded-full text-xs font-medium"
            :class="getLanguageClass(project.language)"
          >
            {{ project.language }}
          </span>
        </div>
      </div>

      <!-- 项目统计数据 -->
      <div class="grid grid-cols-2 gap-4 mb-4">
        <div class="stat-item">
          <div class="flex items-center text-slate-300">
            <i class="fa fa-star text-yellow-400 mr-2"></i>
            <span class="text-sm">Stars</span>
          </div>
          <div class="text-lg font-bold text-white mt-1">
            {{ formatNumber(project.stars) }}
          </div>
        </div>
        <div class="stat-item">
          <div class="flex items-center text-slate-300">
            <i class="fa fa-code-fork text-blue-400 mr-2"></i>
            <span class="text-sm">Forks</span>
          </div>
          <div class="text-lg font-bold text-white mt-1">
            {{ formatNumber(project.forks) }}
          </div>
        </div>
      </div>

      <!-- 额外信息 -->
      <div class="flex justify-between items-center text-slate-400 text-xs">
        <div class="flex items-center">
          <i class="fa fa-users mr-1"></i>
          <span>{{ formatNumber(project.contributor_count) }} 贡献者</span>
        </div>
        <div class="flex items-center">
          <i class="fa fa-calendar mr-1"></i>
          <span>{{ formatDate(project.created_at) }}</span>
        </div>
      </div>
    </div>

    <!-- 卡片底部渐变条 -->
    <div class="h-1 bg-gradient-to-r from-primary to-secondary transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300"></div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Project } from '@/api/reports'

interface Props {
  project: Project
  index?: number
}

const props = withDefaults(defineProps<Props>(), {
  index: 0
})

defineEmits<{
  click: [project: Project]
}>()

const projectName = computed(() => {
  const parts = props.project.name.split('/')
  return parts.length > 1 ? parts[1] : props.project.name
})

const formatNumber = (num: number | string): string => {
  if (typeof num === 'string') return num
  if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`
  if (num >= 1000) return `${(num / 1000).toFixed(1)}K`
  return num.toString()
}

const formatDate = (dateStr: string): string => {
  if (!dateStr || dateStr === 'N/A') return '未知'
  try {
    const date = new Date(dateStr)
    return date.getFullYear().toString()
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
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.project-card:hover {
  background: rgba(30, 41, 59, 0.8);
}

.project-card:hover .stat-item {
  transform: translateY(-1px);
}

.stat-item {
  transition: transform 0.2s ease;
}
</style>