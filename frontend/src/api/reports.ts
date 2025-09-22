import axios, { AxiosError } from 'axios'

// 根据环境变量或开发/生产环境自动选择API地址
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

// 创建axios实例并配置
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    console.log(`🌐 API Request: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('❌ Request Error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.config.url} - ${response.status}`)
    return response
  },
  (error: AxiosError) => {
    console.error(`❌ API Error: ${error.config?.url}`, error.message)
    
    // 统一错误处理
    if (error.code === 'ECONNREFUSED') {
      throw new Error('无法连接到服务器，请检查后端服务是否启动')
    }
    if (error.response?.status === 404) {
      throw new Error('请求的资源不存在')
    }
    if (error.response?.status === 500) {
      throw new Error('服务器内部错误，请稍后重试')
    }
    if (error.code === 'ECONNABORTED') {
      throw new Error('请求超时，请检查网络连接')
    }
    
    throw new Error(error.message || '请求失败')
  }
)

export interface Report {
  date: string
  project_count: number
  content?: string  // 可选，用于详情页
}

export interface ReportContent {
  mdContent: string
}

export interface Project {
  name: string
  url: string
  description: string
  language: string
  stars: number
  forks: number
  contributor_count: number
  created_at: string
  updated_at: string
  open_issues: number
  watchers: number
  summary_date?: string
}

export interface Stats {
  totalReports: number
  totalProjects: number
  topLanguage: string
  weeklyNew: number
  totalForks: string
  avgContributors: number
}

export interface TrendsData {
  time_window_days: number
  most_frequent_projects: {
    name: string
    url: string
    description: string
    language: string
    count: number
    avg_stars: number
  }[]
  most_frequent_languages: [string, number][]
  surging_projects: {
    name: string
    url: string
    description: string
    language: string
    star_increase: number
    start_stars: number
    end_stars: number
  }[]
}

export const reportApi = {
  // 获取报告列表
  async getReports(): Promise<Report[]> {
    try {
      const response = await api.get('/api/reports')
      const reports = response.data
      console.log(`📋 获取到 ${reports.length} 个报告`)
      return reports
    } catch (error) {
      console.error('获取报告列表失败:', error)
      throw error
    }
  },

  // 获取具体报告内容
  async getReportContent(date: string): Promise<Report> {
    try {
      const response = await api.get(`/api/report/${date}`)
      console.log(`📄 获取报告内容: ${date}`)
      return response.data
    } catch (error) {
      console.error(`获取报告内容失败 (${date}):`, error)
      throw error
    }
  },

  // 获取指定日期的项目列表
  async getProjectsByDate(date: string): Promise<Project[]> {
    try {
      const response = await api.get(`/api/projects/${date}`)
      const projects = response.data
      console.log(`🚀 获取到 ${projects.length} 个项目 (${date})`)
      return projects
    } catch (error) {
      console.error(`获取项目列表失败 (${date}):`, error)
      throw error
    }
  },

  // 获取单个项目详情
  async getProjectDetails(projectName: string): Promise<Project> {
    try {
      const response = await api.get(`/api/project/${encodeURIComponent(projectName)}`)
      console.log(`📦 获取项目详情: ${projectName}`)
      return response.data
    } catch (error) {
      console.error(`获取项目详情失败 (${projectName}):`, error)
      throw error
    }
  },

  // 获取统计数据
  async getStats(): Promise<Stats> {
    try {
      const response = await api.get('/api/stats')
      console.log('📊 获取统计数据成功')
      return response.data
    } catch (error) {
      console.error('获取统计数据失败:', error)
      // 返回默认统计数据，避免页面崩溃
      return {
        totalReports: 0,
        totalProjects: 0,
        topLanguage: 'N/A',
        weeklyNew: 0,
        totalForks: '0',
        avgContributors: 0
      }
    }
  },

  // 获取趋势数据
  async getTrends(): Promise<TrendsData> {
    try {
      const response = await api.get('/api/trends')
      console.log('📈 获取趋势数据成功')
      return response.data
    } catch (error) {
      console.error('获取趋势数据失败:', error)
      throw error
    }
  },

  // 健康检查
  async healthCheck(): Promise<boolean> {
    try {
      await api.get('/api/stats')
      return true
    } catch {
      return false
    }
  },
}

// 导出便利函数
export const getReports = reportApi.getReports
export const getProjectsByDate = reportApi.getProjectsByDate
export const getProjectDetails = reportApi.getProjectDetails
export const getReportByDate = reportApi.getReportContent
export const getStats = reportApi.getStats
export const getTrends = reportApi.getTrends
export const healthCheck = reportApi.healthCheck

// 导出API基础URL用于调试
export const getApiBaseUrl = () => API_BASE_URL

export default api