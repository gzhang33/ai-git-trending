// Markdown-it插件类型声明
declare module 'markdown-it-emoji';
declare module 'markdown-it-task-lists';
declare module 'markdown-it-abbr';
declare module 'markdown-it-footnote';

// 为markdown-it插件提供更具体的类型定义
declare module 'markdown-it-anchor' {
  import type { PluginWithOptions } from 'markdown-it'
  const anchor: PluginWithOptions<{
    permalink?: boolean
    permalinkSymbol?: string
    permalinkBefore?: boolean
  }>
  export default anchor
}

declare module 'markdown-it-toc-done-right' {
  import type { PluginSimple } from 'markdown-it'
  const toc: PluginSimple
  export default toc
}