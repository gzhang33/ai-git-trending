import MarkdownIt from 'markdown-it'

// 初始化 markdown-it 解析器
export const md = new MarkdownIt({
  html: true,          // 允许 HTML 标签
  breaks: true,        // 自动转换换行
  linkify: true,       // 自动识别链接
  typographer: true    // 启用排版优化
})

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
    }
  }
  return defaultRender(tokens, idx, options, env, self)
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
        'bg-gradient-to-r', 'from-slate-800', 'to-slate-700',
        'border', 'border-slate-600', 'rounded-xl', 'p-4', 'my-8',
        'shadow-lg', 'transition-transform', 'duration-200',
        'hover:-translate-y-1', 'hover:shadow-xl'
      )
    }
  })
  
  // 为外部链接添加图标
  const links = container.querySelectorAll('a[href^="http"]')
  links.forEach(link => {
    if (!link.querySelector('.external-icon')) {
      const icon = document.createElement('i')
      icon.className = 'fa fa-external-link external-icon ml-1 text-xs opacity-70'
      link.appendChild(icon)
    }
  })
  
  // 为代码块添加复制功能
  const codeBlocks = container.querySelectorAll('pre code')
  codeBlocks.forEach(block => {
    const pre = block.parentElement!
    if (!pre.querySelector('.copy-btn')) {
      const copyBtn = document.createElement('button')
      copyBtn.className = 'copy-btn absolute top-2 right-2 bg-blue-500/20 border border-blue-500/30 text-blue-400 px-2 py-1 rounded text-xs transition-all duration-200 hover:bg-blue-500/30'
      copyBtn.innerHTML = '<i class="fa fa-copy"></i>'
      
      copyBtn.addEventListener('click', async () => {
        try {
          await navigator.clipboard.writeText(block.textContent || '')
          copyBtn.innerHTML = '<i class="fa fa-check"></i>'
          copyBtn.classList.remove('text-blue-400', 'bg-blue-500/20', 'border-blue-500/30')
          copyBtn.classList.add('text-green-400', 'bg-green-500/20', 'border-green-500/30')
          setTimeout(() => {
            copyBtn.innerHTML = '<i class="fa fa-copy"></i>'
            copyBtn.classList.remove('text-green-400', 'bg-green-500/20', 'border-green-500/30')
            copyBtn.classList.add('text-blue-400', 'bg-blue-500/20', 'border-blue-500/30')
          }, 2000)
        } catch (err) {
          console.error('复制失败:', err)
        }
      })
      
      pre.style.position = 'relative'
      pre.appendChild(copyBtn)
    }
  })
}