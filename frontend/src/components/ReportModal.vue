<template>
  <Teleport to="body">
    <div class="fixed inset-0 bg-black/70 z-50 flex items-center justify-center p-4 animate-fadeIn">
      <div 
        class="bg-slate-800 rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col animate-fadeIn"
        @click.stop
      >
        <!-- 模态框头部 -->
        <div class="p-6 border-b border-white/10 flex justify-between items-center">
          <h3 class="text-xl font-bold text-white">
            报告 - {{ formatDate(report.date) }}
          </h3>
          <button
            @click="$emit('close')"
            class="p-2 rounded-full hover:bg-white/10 transition-colors text-white"
          >
            <i class="fa fa-times text-xl"></i>
          </button>
        </div>

        <!-- 模态框内容 -->
        <div class="flex-grow overflow-y-auto p-8 markdown-content max-w-none">
          <div v-if="loading" class="h-full flex flex-col items-center justify-center">
            <div class="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-4"></div>
            <p class="text-slate-400">加载报告中...</p>
          </div>
          <div 
            v-else
            ref="markdownContainer"
            class="markdown-content"
            v-html="renderedContent"
          ></div>
        </div>

        <!-- 模态框底部 -->
        <div class="p-6 border-t border-white/10 flex justify-between items-center">
          <div class="text-slate-400 text-sm">
            {{ report.project_count }} 个项目 | {{ wordCount }} 字
          </div>
          <div class="flex space-x-3">
            <button
              @click="exportReport"
              class="bg-blue-500/20 text-blue-400 border border-blue-500/30 px-4 py-2 rounded-lg text-sm hover:bg-blue-500/30 transition-colors flex items-center"
            >
              <i class="fa fa-download mr-2"></i>
              导出
            </button>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import { renderMarkdown, enhanceMarkdownDisplay } from '../utils/markdown'
import type { Report } from '../api/reports'

// Props
const props = defineProps<{
  report: Report
}>()

// Emits
const emit = defineEmits<{
  close: []
}>()

// 响应式数据
const loading = ref(false)
const markdownContainer = ref<HTMLElement>()

// 计算属性
const renderedContent = computed(() => {
  if (!props.report.content) return ''
  return renderMarkdown(props.report.content)
})

const wordCount = computed(() => {
  if (!props.report.content) return 0
  return props.report.content.replace(/\s/g, '').length
})

// 生命周期钩子
onMounted(async () => {
  await nextTick()
  if (markdownContainer.value) {
    enhanceMarkdownDisplay(markdownContainer.value)
  }
})

// 方法
function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  })
}

function exportReport() {
  if (!props.report.content) return
  
  const blob = new Blob([props.report.content], { type: 'text/markdown;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `github_trending_${props.report.date}.md`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

// 键盘事件处理
onMounted(() => {
  const handleEscape = (e: KeyboardEvent) => {
    if (e.key === 'Escape') {
      emit('close')
    }
  }
  document.addEventListener('keydown', handleEscape)
  
  // 清理事件监听器
  return () => {
    document.removeEventListener('keydown', handleEscape)
  }
})
</script>
