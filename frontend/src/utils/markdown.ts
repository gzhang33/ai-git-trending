import MarkdownIt from 'markdown-it'
// @ts-ignore
import markdownItTaskList from 'markdown-it-task-lists'
// @ts-ignore
import markdownItAnchor from 'markdown-it-anchor'
// @ts-ignore
import markdownItToc from 'markdown-it-toc-done-right'
// @ts-ignore
import markdownItEmoji from 'markdown-it-emoji'
// @ts-ignore
import markdownItSub from 'markdown-it-sub'
// @ts-ignore
import markdownItSup from 'markdown-it-sup'
// @ts-ignore
import markdownItMark from 'markdown-it-mark'
// @ts-ignore
import markdownItIns from 'markdown-it-ins'
// @ts-ignore
import markdownItAbbr from 'markdown-it-abbr'
// @ts-ignore
import markdownItFootnote from 'markdown-it-footnote'

// 初始化 markdown-it 解析器
export const md = new MarkdownIt({
  html: true,          // 允许 HTML 标签
  breaks: true,        // 自动转换换行
  linkify: true,       // 自动识别链接
  typographer: true,   // 启用排版优化
  quotes: '“”‘’'   // 中文引号
})

// 添加插件
md.use(markdownItTaskList, { enabled: true })
md.use(markdownItAnchor)
md.use(markdownItToc)
md.use(markdownItEmoji)
md.use(markdownItSub)
md.use(markdownItSup)
md.use(markdownItMark)
md.use(markdownItIns)
md.use(markdownItAbbr)
md.use(markdownItFootnote)

// 自定义渲染规则
const defaultRender = md.renderer.rules.link_open || function(tokens, idx, options, env, self) {
  return self.renderToken(tokens, idx, options)
}

// 为外部链接添加 target="_blank"
md.renderer.rules.link_open = function (tokens, idx, options, env, self) {
  const token = tokens[idx]
  const hrefIndex = token.attrIndex('href')
  if (hrefIndex >= 0) {
    const href = token.attrs![hrefIndex][1]
    if (href.startsWith('http')) {
      token.attrPush(['target', '_blank'])
      token.attrPush(['rel', 'noopener noreferrer'])
      token.attrPush(['class', 'external-link'])
    }
  }
  return defaultRender(tokens, idx, options, env, self)
}

// 自定义标题渲染
md.renderer.rules.heading_open = function (tokens, idx, options, env, self) {
  const token = tokens[idx]
  const level = token.markup.length
  
  // 为不同级别的标题添加不同的样式
  const classes = [
    'heading',
    `heading-${level}`,
    'font-bold',
    'text-slate-100',
    'mb-4',
    'mt-6'
  ]
  
  if (level === 1) {
    classes.push('text-4xl', 'text-blue-300', 'border-b', 'border-slate-600', 'pb-2')
  } else if (level === 2) {
    classes.push('text-3xl', 'text-blue-300')
  } else if (level === 3) {
    classes.push('text-2xl', 'text-purple-300')
  } else {
    classes.push('text-xl', 'text-slate-300')
  }
  
  token.attrPush(['class', classes.join(' ')])
  return self.renderToken(tokens, idx, options)
}

// 自定义代码块渲染
md.renderer.rules.code_block = function (tokens, idx, options, env, self) {
  const token = tokens[idx]
  const content = token.content
  const lang = token.info || ''
  
  return `<div class="code-block-container relative mb-6">
    <div class="code-block-header bg-slate-800 px-4 py-2 rounded-t-lg border border-slate-600 border-b-0 flex justify-between items-center">
      <span class="text-slate-400 text-sm font-medium">${lang || 'text'}</span>
      <button class="copy-code-btn text-slate-400 hover:text-blue-400 transition-colors" data-code="${encodeURIComponent(content)}">
        <i class="fa fa-copy text-sm"></i>
      </button>
    </div>
    <pre class="code-block bg-slate-900 p-4 rounded-b-lg border border-slate-600 border-t-0 overflow-x-auto"><code class="language-${lang}">${md.utils.escapeHtml(content)}</code></pre>
  </div>`
}

// 自定义列表渲染
md.renderer.rules.bullet_list_open = function (tokens, idx, options, env, self) {
  return '<ul class="list-disc list-inside space-y-2 text-slate-300 mb-4">\n'
}

md.renderer.rules.ordered_list_open = function (tokens, idx, options, env, self) {
  return '<ol class="list-decimal list-inside space-y-2 text-slate-300 mb-4">\n'
}

// 自定义表格渲染
md.renderer.rules.table_open = function (tokens, idx, options, env, self) {
  return '<div class="table-container overflow-x-auto mb-6"><table class="min-w-full bg-slate-800/50 border border-slate-600 rounded-lg">\n'
}

md.renderer.rules.table_close = function (tokens, idx, options, env, self) {
  return '</table></div>\n'
}

md.renderer.rules.thead_open = function (tokens, idx, options, env, self) {
  return '<thead class="bg-slate-700">\n'
}

md.renderer.rules.th_open = function (tokens, idx, options, env, self) {
  return '<th class="px-4 py-3 text-left text-slate-200 font-semibold border-b border-slate-600">'
}

md.renderer.rules.td_open = function (tokens, idx, options, env, self) {
  return '<td class="px-4 py-3 text-slate-300 border-b border-slate-700">'
}

// 自定义引用渲染
md.renderer.rules.blockquote_open = function (tokens, idx, options, env, self) {
  return '<blockquote class="border-l-4 border-blue-500 pl-4 py-2 my-4 bg-slate-800/30 rounded-r-lg">\n'
}

// 导出渲染函数
export function renderMarkdown(content: string): string {
  return md.render(content)
}

// 增强显示效果的后处理函数
export function enhanceMarkdownDisplay(container: HTMLElement) {
  // 为项目标题添加特殊样式
  const projectHeaders = container.querySelectorAll('h3')
  projectHeaders.forEach(header => {
    if (header.textContent?.includes('✨')) {
      header.classList.add(
        'project-header',
        'bg-gradient-to-r', 'from-slate-800/80', 'to-slate-700/80',
        'border', 'border-slate-600/50', 'rounded-xl', 'p-4', 'my-6',
        'shadow-lg', 'transition-all', 'duration-300',
        'hover:-translate-y-1', 'hover:shadow-xl', 'hover:border-blue-500/30',
        'backdrop-blur-sm'
      )
      
      // 添加星星动画
      const starElement = header.querySelector('span') || document.createElement('span')
      starElement.innerHTML = '✨'
      starElement.className = 'inline-block animate-pulse text-yellow-400 mr-2'
    }
  })
  
  // 为所有标题添加鼠标悬停效果
  const allHeaders = container.querySelectorAll('h1, h2, h3, h4, h5, h6')
  allHeaders.forEach(header => {
    header.classList.add('transition-all', 'duration-200', 'hover:text-blue-400', 'cursor-pointer')
    
    // 添加点击复制功能
    header.addEventListener('click', () => {
      const text = header.textContent || ''
      navigator.clipboard.writeText(text).then(() => {
        // 显示复制成功提示
        showToast('标题已复制到剪贴板', 'success')
      })
    })
  })
  
  // 为外部链接添加图标和样式
  const links = container.querySelectorAll('a[href^="http"]')
  links.forEach(link => {
    link.classList.add(
      'text-blue-400', 'hover:text-blue-300', 'transition-colors',
      'underline', 'decoration-blue-400/30', 'hover:decoration-blue-300',
      'underline-offset-2'
    )
    
    if (!link.querySelector('.external-icon')) {
      const icon = document.createElement('i')
      icon.className = 'fa fa-external-link external-icon ml-1 text-xs opacity-70'
      link.appendChild(icon)
    }
    
    // 添加悬停效果
    link.addEventListener('mouseenter', () => {
      const icon = link.querySelector('.external-icon') as HTMLElement
      if (icon) {
        icon.style.transform = 'scale(1.1) rotate(12deg)'
        icon.style.transition = 'transform 0.2s ease'
      }
    })
    
    link.addEventListener('mouseleave', () => {
      const icon = link.querySelector('.external-icon') as HTMLElement
      if (icon) {
        icon.style.transform = 'scale(1) rotate(0deg)'
      }
    })
  })
  
  // 为代码块添加复制功能和语法高亮
  const codeBlocks = container.querySelectorAll('pre code')
  codeBlocks.forEach(block => {
    const pre = block.parentElement!
    pre.classList.add('relative', 'group')
    
    if (!pre.querySelector('.copy-btn')) {
      const copyBtn = document.createElement('button')
      copyBtn.className = 'copy-btn absolute top-3 right-3 bg-slate-700/80 hover:bg-blue-600/80 border border-slate-600 hover:border-blue-500 text-slate-300 hover:text-white px-3 py-1.5 rounded-md text-xs font-medium transition-all duration-200 opacity-0 group-hover:opacity-100 flex items-center space-x-1 backdrop-blur-sm'
      copyBtn.innerHTML = '<i class="fa fa-copy"></i><span>Copy</span>'
      
      copyBtn.addEventListener('click', async () => {
        try {
          await navigator.clipboard.writeText(block.textContent || '')
          copyBtn.innerHTML = '<i class="fa fa-check text-green-400"></i><span class="text-green-400">Copied!</span>'
          copyBtn.classList.remove('bg-slate-700/80', 'hover:bg-blue-600/80', 'border-slate-600')
          copyBtn.classList.add('bg-green-600/80', 'border-green-500')
          
          setTimeout(() => {
            copyBtn.innerHTML = '<i class="fa fa-copy"></i><span>Copy</span>'
            copyBtn.classList.remove('bg-green-600/80', 'border-green-500')
            copyBtn.classList.add('bg-slate-700/80', 'hover:bg-blue-600/80', 'border-slate-600')
          }, 2000)
        } catch (err) {
          console.error('复制失败:', err)
          showToast('复制失败', 'error')
        }
      })
      
      pre.appendChild(copyBtn)
    }
    
    // 添加代码语言标签
    const langMatch = block.className.match(/language-(小\w+)/)
    if (langMatch && !pre.querySelector('.lang-label')) {
      const langLabel = document.createElement('div')
      langLabel.className = 'lang-label absolute top-3 left-3 bg-slate-800/90 text-slate-300 px-2 py-1 rounded text-xs font-mono border border-slate-600'
      langLabel.textContent = langMatch[1].toUpperCase()
      pre.appendChild(langLabel)
    }
  })
  
  // 为表格添加响应式样式
  const tables = container.querySelectorAll('table')
  tables.forEach(table => {
    table.classList.add('border-collapse', 'border-spacing-0')
    
    // 添加排序功能
    const headers = table.querySelectorAll('th')
    headers.forEach(header => {
      header.classList.add('cursor-pointer', 'hover:bg-slate-600/50', 'transition-colors')
      header.addEventListener('click', () => {
        // 这里可以添加表格排序逻辑
        showToast('表格排序功能正在开发中', 'info')
      })
    })
  })
  
  // 为任务列表添加交互效果
  const taskItems = container.querySelectorAll('input[type="checkbox"]')
  taskItems.forEach(checkbox => {
    const input = checkbox as HTMLInputElement
    const listItem = input.closest('li')
    if (listItem) {
      listItem.classList.add('transition-all', 'duration-200', 'hover:bg-slate-800/30', 'rounded', 'px-2', 'py-1')
      
      if (input.checked) {
        listItem.classList.add('opacity-75', 'line-through')
      }
    }
  })
  
  // 添加图片懒加载和等比缩放
  const images = container.querySelectorAll('img')
  images.forEach(img => {
    img.classList.add('max-w-full', 'h-auto', 'rounded-lg', 'shadow-lg', 'transition-transform', 'duration-200', 'hover:scale-105', 'cursor-pointer')
    
    // 添加点击放大功能
    img.addEventListener('click', () => {
      openImageModal(img.src, img.alt || '')
    })
  })
  
  // 为引用块添加动画效果
  const blockquotes = container.querySelectorAll('blockquote')
  blockquotes.forEach(blockquote => {
    blockquote.classList.add('animate-fadeIn', 'hover:border-blue-400', 'transition-colors', 'duration-300')
  })
}

// 辅助函数
function showToast(message: string, type: 'success' | 'error' | 'info' = 'info') {
  // 创建简单的提示框
  const toast = document.createElement('div')
  toast.className = `fixed top-4 right-4 z-50 px-4 py-2 rounded-lg shadow-lg transition-all duration-300 transform translate-x-full opacity-0`
  
  switch (type) {
    case 'success':
      toast.classList.add('bg-green-600', 'text-white')
      break
    case 'error':
      toast.classList.add('bg-red-600', 'text-white')
      break
    default:
      toast.classList.add('bg-blue-600', 'text-white')
  }
  
  toast.textContent = message
  document.body.appendChild(toast)
  
  // 显示动画
  setTimeout(() => {
    toast.classList.remove('translate-x-full', 'opacity-0')
  }, 100)
  
  // 自动隐藏
  setTimeout(() => {
    toast.classList.add('translate-x-full', 'opacity-0')
    setTimeout(() => {
      document.body.removeChild(toast)
    }, 300)
  }, 3000)
}

function openImageModal(src: string, alt: string) {
  // 创建图片模态框
  const modal = document.createElement('div')
  modal.className = 'fixed inset-0 bg-black/80 z-50 flex items-center justify-center p-4 animate-fadeIn'
  modal.innerHTML = `
    <div class="relative max-w-4xl max-h-full">
      <img src="${src}" alt="${alt}" class="max-w-full max-h-full object-contain rounded-lg shadow-2xl">
      <button class="absolute top-4 right-4 text-white bg-black/50 hover:bg-black/70 rounded-full w-8 h-8 flex items-center justify-center transition-colors">
        <i class="fa fa-times"></i>
      </button>
      ${alt ? `<div class="absolute bottom-4 left-4 right-4 text-white bg-black/50 rounded-lg p-2 text-center">${alt}</div>` : ''}
    </div>
  `
  
  // 添加关闭事件
  modal.addEventListener('click', (e) => {
    if (e.target === modal || (e.target as HTMLElement).closest('button')) {
      document.body.removeChild(modal)
    }
  })
  
  document.body.appendChild(modal)
}