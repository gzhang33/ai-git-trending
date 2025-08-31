import MarkdownIt from 'markdown-it'

// 创建简化的markdown-it实例
const md = new MarkdownIt({
  html: true,
  breaks: true,
  linkify: true,
  typographer: true
})

// 简单的渲染函数
export function renderMarkdown(content: string): string {
  return md.render(content)
}

// 简化的增强显示函数
export function enhanceMarkdownDisplay(container: HTMLElement) {
  // 为代码块添加复制功能
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
        }
      })
      
      pre.appendChild(copyBtn)
    }
  })
  
  // 为外部链接添加图标
  const links = container.querySelectorAll('a')
  links.forEach(link => {
    const href = link.getAttribute('href')
    if (href && href.startsWith('http') && !href.includes(window.location.hostname)) {
      link.setAttribute('target', '_blank')
      link.setAttribute('rel', 'noopener noreferrer')
      
      if (!link.classList.contains('external-link')) {
        link.classList.add('external-link')
        const icon = document.createElement('span')
        icon.className = 'inline-block ml-1 text-xs opacity-70'
        icon.innerHTML = '<i class="fa fa-external-link-alt"></i>'
        link.appendChild(icon)
      }
    }
  })
}