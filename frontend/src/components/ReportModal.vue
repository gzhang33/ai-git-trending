<template>
  <Teleport to="body">
    <div class="fixed inset-0 bg-black/80 z-50 flex items-center justify-center p-2 sm:p-4 animate-fadeIn backdrop-blur-sm">
      <div 
        class="glass-card rounded-2xl lg:rounded-3xl max-w-6xl w-full max-h-[95vh] overflow-hidden flex flex-col animate-fadeInUp shadow-2xl"
        @click.stop
      >
        <!-- 模态框头部 -->
        <header class="relative p-4 lg:p-6 border-b border-white/10 bg-gradient-to-r from-slate-800/50 to-slate-700/50">
          <div class="flex justify-between items-center">
              <div class="flex items-center space-x-3 lg:space-x-4 flex-1 min-w-0">
                <div class="w-10 h-10 lg:w-12 lg:h-12 bg-gradient-primary rounded-xl flex items-center justify-center flex-shrink-0">
                  <svg class="w-5 h-5 lg:w-6 lg:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                </div>
                <div class="min-w-0 flex-1">
                  <h3 style="background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899); background-clip: text; -webkit-background-clip: text; color: transparent;" class="text-lg lg:text-2xl font-bold truncate">
                    GitHub 热门项目报告
                  </h3>
                  <p class="text-xs lg:text-sm text-slate-400 mt-1 truncate">
                    {{ formatDate(report.date) }}
                  </p>
                </div>
              </div>
            
            <div class="flex items-center space-x-2 lg:space-x-3 flex-shrink-0">
                <!-- 导出按钮 - 添加在标题区域 -->
                <div class="relative mr-2">
                  <button
                    @click="showHeaderExportMenu = !showHeaderExportMenu"
                    class="btn-icon"
                    title="导出报告"
                  >
                    <svg class="w-4 h-4 lg:w-5 lg:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path>
                    </svg>
                  </button>
                  
                  <!-- 导出菜单 -->
                  <div v-if="showHeaderExportMenu" class="absolute top-full right-0 mt-2 w-40 glass-card rounded-xl py-2 shadow-xl z-50">
                    <button @click="exportReport('md')" class="export-menu-item">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                      </svg>
                      Markdown
                    </button>
                    <button @click="exportReport('html')" class="export-menu-item">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
                      </svg>
                      HTML
                    </button>
                  </div>
                </div>
                
                <!-- 全屏按钮 -->
              <button
                @click="toggleFullscreen"
                class="btn-icon hidden lg:flex"
                title="全屏模式"
              >
                <svg v-if="!isFullscreen" class="w-4 h-4 lg:w-5 lg:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"></path>
                </svg>
                <svg v-else class="w-4 h-4 lg:w-5 lg:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 9V4.5M9 9H4.5M9 9L3.75 3.75M15 9v-4.5M15 9h4.5M15 9l5.25-5.25M9 15v4.5M9 15H4.5M9 15l-5.25 5.25M15 15v4.5M15 15h4.5m0 0l5.25 5.25"></path>
                </svg>
              </button>
              
              <!-- 关闭按钮 -->
              <button
                @click="$emit('close')"
                class="btn-icon hover:bg-red-500/20 hover:border-red-500/30 hover:text-red-400"
                title="关闭"
              >
                <svg class="w-4 h-4 lg:w-5 lg:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>
          </div>
          
          <!-- 进度条 -->
          <div class="absolute bottom-0 left-0 w-full h-0.5 lg:h-1 bg-slate-700/50">
            <div 
              class="h-full bg-gradient-primary transition-all duration-300 ease-out"
              :style="{ width: scrollProgress + '%' }"
            ></div>
          </div>
        </header>

        <!-- 模态框内容 -->
        <main 
          ref="contentContainer"
          class="flex-grow overflow-y-auto relative"
          @scroll="updateScrollProgress"
        >
          <div v-if="loading" class="h-full flex flex-col items-center justify-center py-20">
            <div class="relative mb-8">
              <div class="w-16 h-16 border-4 border-blue-500/30 rounded-full animate-spin"></div>
              <div class="absolute top-0 left-0 w-16 h-16 border-4 border-transparent border-t-blue-500 rounded-full animate-spin"></div>
            </div>
            <h4 class="text-lg font-medium text-slate-300 mb-2">加载中</h4>
            <p class="text-slate-400">正在解析报告内容...</p>
          </div>
          
          <div v-else class="p-4 lg:p-8">
            <!-- 报告统计信息 -->
            <div class="mb-6 lg:mb-8 grid grid-cols-2 lg:grid-cols-4 gap-3 lg:gap-4">
              <div class="glass-card rounded-xl p-3 lg:p-4 text-center hover:shadow-lg transition-shadow">
                <div class="text-lg lg:text-2xl font-bold text-blue-400 mb-1">{{ report.project_count }}</div>
                <div class="text-xs lg:text-sm text-slate-400">项目数量</div>
              </div>
              <div class="glass-card rounded-xl p-3 lg:p-4 text-center hover:shadow-lg transition-shadow">
                <div class="text-lg lg:text-2xl font-bold text-green-400 mb-1">{{ wordCount.toLocaleString() }}</div>
                <div class="text-xs lg:text-sm text-slate-400">字数统计</div>
              </div>
              <div class="glass-card rounded-xl p-3 lg:p-4 text-center hover:shadow-lg transition-shadow">
                <div class="text-lg lg:text-2xl font-bold text-purple-400 mb-1">{{ readingTime }}</div>
                <div class="text-xs lg:text-sm text-slate-400">阅读时间</div>
              </div>
              <div class="glass-card rounded-xl p-3 lg:p-4 text-center hover:shadow-lg transition-shadow">
                <div class="text-lg lg:text-2xl font-bold text-pink-400 mb-1">{{ formatDate(report.date).split(' ')[0] }}</div>
                <div class="text-xs lg:text-sm text-slate-400">发布日期</div>
              </div>
            </div>
            
            <!-- 快速导航 -->
            <div class="mb-6 lg:mb-8 p-3 lg:p-4 bg-slate-800/30 rounded-xl border border-slate-600/30">
              <div class="flex items-center mb-3">
                <i class="fa fa-compass mr-2 text-blue-400"></i>
                <span class="font-semibold text-slate-200 text-sm lg:text-base">快速导航</span>
              </div>
              <div class="flex flex-wrap gap-1 lg:gap-2" id="quick-nav">
                <!-- 导航链接将由JavaScript生成 -->
              </div>
            </div>
            
            <!-- Markdown 内容 -->
            <div 
              ref="markdownContainer"
              class="markdown-content prose prose-invert max-w-none bg-slate-900/30 rounded-xl p-4 lg:p-6 border border-slate-600/30 text-sm lg:text-base"
              v-html="renderedContent"
            ></div>
          </div>
          
          <!-- 返回顶部按钮 -->
          <button 
            v-show="showBackToTop"
            @click="scrollToTop"
            class="fixed bottom-8 right-8 btn-primary w-12 h-12 rounded-full shadow-lg animate-bounce-gentle z-10"
            title="返回顶部"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 11l5-5m0 0l5 5m-5-5v12"></path>
            </svg>
          </button>
        </main>

        <!-- 模态框底部 -->
        <footer class="p-4 lg:p-6 border-t border-white/10 bg-slate-800/30">
          <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center space-y-4 lg:space-y-0">
            <div class="flex flex-wrap items-center gap-4 lg:gap-6 text-xs lg:text-sm text-slate-400">
              <div class="flex items-center space-x-1 lg:space-x-2">
                <svg class="w-3 h-3 lg:w-4 lg:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                </svg>
                <span>{{ report.project_count }} 个项目</span>
              </div>
              <div class="flex items-center space-x-1 lg:space-x-2">
                <svg class="w-3 h-3 lg:w-4 lg:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                </svg>
                <span>{{ wordCount.toLocaleString() }} 字</span>
              </div>
              <div class="flex items-center space-x-1 lg:space-x-2">
                <svg class="w-3 h-3 lg:w-4 lg:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <span>{{ readingTime }}</span>
              </div>
            </div>
            
            <div class="flex flex-wrap gap-2 lg:gap-3 w-full lg:w-auto">
              <button
                @click="copyToClipboard"
                class="btn-secondary flex-1 lg:flex-none text-xs lg:text-sm"
                title="复制到剪贴板"
              >
                <svg class="w-3 h-3 lg:w-4 lg:h-4 mr-1 lg:mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                </svg>
                复制
              </button>
              
              <button
                @click="shareReport"
                class="btn-secondary flex-1 lg:flex-none text-xs lg:text-sm"
                title="分享报告"
              >
                <svg class="w-3 h-3 lg:w-4 lg:h-4 mr-1 lg:mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z"></path>
                </svg>
                分享
              </button>
              
              <div class="relative" ref="exportDropdown">
                <button
                  @click="showExportMenu = !showExportMenu"
                  class="btn-primary flex-1 lg:flex-none text-xs lg:text-sm"
                  title="导出报告"
                >
                  <svg class="w-3 h-3 lg:w-4 lg:h-4 mr-1 lg:mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                  导出
                  <svg class="w-3 h-3 lg:w-4 lg:h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                  </svg>
                </button>
                
                <!-- 导出菜单 -->
                <div v-if="showExportMenu" class="absolute bottom-full right-0 mb-2 w-48 glass-card rounded-xl py-2 shadow-xl">
                  <button @click="exportReport('md')" class="export-menu-item">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                    </svg>
                    Markdown 格式
                  </button>
                  <button @click="exportReport('html')" class="export-menu-item">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
                    </svg>
                    HTML 格式
                  </button>
                  <button @click="exportReport('pdf')" class="export-menu-item">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
                    </svg>
                    PDF 格式
                  </button>
                </div>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick, onUnmounted } from 'vue'
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
const contentContainer = ref<HTMLElement>()
const exportDropdown = ref<HTMLElement>()
const showExportMenu = ref(false)
const showHeaderExportMenu = ref(false)
const isFullscreen = ref(false)
const scrollProgress = ref(0)
const showBackToTop = ref(false)

// 计算属性
const renderedContent = computed(() => {
  if (!props.report.content) return ''
  return renderMarkdown(props.report.content)
})

const wordCount = computed(() => {
  if (!props.report.content) return 0
  return props.report.content.replace(/\s/g, '').length
})

const readingTime = computed(() => {
  const wordsPerMinute = 300 // 中文阅读速度
  const minutes = Math.ceil(wordCount.value / wordsPerMinute)
  return `${minutes} 分钟`
})

// 生命周期钩子
onMounted(async () => {
  await nextTick()
  if (markdownContainer.value) {
    enhanceMarkdownDisplay(markdownContainer.value)
    generateQuickNavigation()
  }
  
  // 添加事件监听器
  document.addEventListener('keydown', handleKeydown)
  document.addEventListener('click', handleOutsideClick)
  
  // 防止背景滚动
  document.body.style.overflow = 'hidden'
})

onUnmounted(() => {
  // 清理事件监听器
  document.removeEventListener('keydown', handleKeydown)
  document.removeEventListener('click', handleOutsideClick)
  
  // 恢复背景滚动
  document.body.style.overflow = ''
  
  // 退出全屏模式
  if (isFullscreen.value) {
    exitFullscreen()
  }
})

// 事件处理函数
function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape') {
    emit('close')
  } else if (e.key === 'F11') {
    e.preventDefault()
    toggleFullscreen()
  }
}

function handleOutsideClick(e: Event) {
  if (showExportMenu.value && exportDropdown.value && !exportDropdown.value.contains(e.target as Node)) {
    showExportMenu.value = false
  }
  
  // 关闭标题区域的导出菜单
  const headerExportButton = document.querySelector('[title="导出报告"]')
  const headerExportMenu = document.querySelector('.relative.mr-2 > div')
  
  if (showHeaderExportMenu.value && 
      headerExportButton && 
      headerExportMenu && 
      !headerExportButton.contains(e.target as Node) && 
      !headerExportMenu.contains(e.target as Node)) {
    showHeaderExportMenu.value = false
  }
}

function updateScrollProgress() {
  if (!contentContainer.value) return
  
  const { scrollTop, scrollHeight, clientHeight } = contentContainer.value
  const progress = (scrollTop / (scrollHeight - clientHeight)) * 100
  scrollProgress.value = Math.min(100, Math.max(0, progress))
  
  // 显示/隐藏返回顶部按钮
  showBackToTop.value = scrollTop > 300
}

function scrollToTop() {
  if (contentContainer.value) {
    contentContainer.value.scrollTo({
      top: 0,
      behavior: 'smooth'
    })
  }
}

function toggleFullscreen() {
  if (!isFullscreen.value) {
    enterFullscreen()
  } else {
    exitFullscreen()
  }
}

function enterFullscreen() {
  if (document.documentElement.requestFullscreen) {
    document.documentElement.requestFullscreen()
    isFullscreen.value = true
  }
}

function exitFullscreen() {
  if (document.exitFullscreen && document.fullscreenElement) {
    document.exitFullscreen()
    isFullscreen.value = false
  }
}
// 工具函数
function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  })
}

function exportReport(format: 'md' | 'html' | 'pdf' = 'md') {
  if (!props.report.content) return
  
  let content: string
  let mimeType: string
  let extension: string
  
  switch (format) {
    case 'html':
      content = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GitHub 热门项目报告 - ${props.report.date}</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }
    h1, h2, h3 { color: #2c3e50; }
    code { background: #f4f4f4; padding: 2px 4px; border-radius: 3px; }
    pre { background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }
  </style>
</head>
<body>
${renderedContent.value}
</body>
</html>`
      mimeType = 'text/html'
      extension = 'html'
      break
    case 'pdf':
      // PDF 导出需要额外的库，这里先显示提示
      alert('🚧 PDF 导出功能正在开发中，请使用浏览器的打印功能代替')
      window.print()
      return
    default:
      content = props.report.content
      mimeType = 'text/markdown'
      extension = 'md'
  }
  
  const blob = new Blob([content], { type: `${mimeType};charset=utf-8` })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `github_trending_${props.report.date}.${extension}`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
  
  showExportMenu.value = false
  console.log(`📥 报告已导出为 ${format.toUpperCase()} 格式`)
}

async function copyToClipboard() {
  if (!props.report.content) return
  
  try {
    await navigator.clipboard.writeText(props.report.content)
    // 显示成功提示（可以后续添加 toast 组件）
    console.log('📋 内容已复制到剪贴板')
  } catch (err) {
    console.error('复制失败:', err)
  }
}

function shareReport() {
  if (navigator.share) {
    navigator.share({
      title: `GitHub 热门项目报告 - ${props.report.date}`,
      text: `查看 ${props.report.date} 的 GitHub 热门项目分析报告`,
      url: window.location.href
    })
  } else {
    // 降级方案：复制链接
    copyToClipboard()
  }
}

// 生成快速导航
function generateQuickNavigation() {
  if (!markdownContainer.value) return
  
  const headers = markdownContainer.value.querySelectorAll('h1, h2, h3, h4')
  const quickNavContainer = document.getElementById('quick-nav')
  
  if (!quickNavContainer || headers.length === 0) return
  
  // 清空现有内容
  quickNavContainer.innerHTML = ''
  
  headers.forEach((header, index) => {
    const level = parseInt(header.tagName.charAt(1))
    const text = header.textContent || ''
    const id = `heading-${index}`
    
    // 为标题添加ID
    header.id = id
    
    // 创建导航按钮
    const navButton = document.createElement('button')
    navButton.className = `text-xs px-3 py-1.5 rounded-lg transition-all duration-200 border ${
      level === 1 ? 'bg-blue-500/20 text-blue-300 border-blue-500/30 hover:bg-blue-500/30' :
      level === 2 ? 'bg-purple-500/20 text-purple-300 border-purple-500/30 hover:bg-purple-500/30' :
      level === 3 ? 'bg-green-500/20 text-green-300 border-green-500/30 hover:bg-green-500/30' :
      'bg-gray-500/20 text-gray-300 border-gray-500/30 hover:bg-gray-500/30'
    }`
    navButton.textContent = text.length > 20 ? text.substring(0, 20) + '...' : text
    navButton.title = text
    
    navButton.addEventListener('click', () => {
      header.scrollIntoView({ behavior: 'smooth', block: 'start' })
      // 添加高亮效果
      header.classList.add('highlight-flash')
      setTimeout(() => {
        header.classList.remove('highlight-flash')
      }, 2000)
    })
    
    quickNavContainer.appendChild(navButton)
  })
  
  // 如果没有标题，隐藏导航区域
  const navSection = quickNavContainer.closest('.mb-8') as HTMLElement | null
  if (navSection) {
    navSection.style.display = headers.length > 0 ? 'block' : 'none'
  }
}

// 添加高亮动画样式
function addHighlightStyles() {
  const style = document.createElement('style')
  style.textContent = `
    .highlight-flash {
      animation: highlight-flash 2s ease-in-out;
    }
    
    @keyframes highlight-flash {
      0% { background-color: rgba(59, 130, 246, 0.3); }
      50% { background-color: rgba(59, 130, 246, 0.1); }
      100% { background-color: transparent; }
    }
  `
  document.head.appendChild(style)
}

// 在组件加载时添加样式
addHighlightStyles()
</script>
