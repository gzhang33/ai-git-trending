import axios from 'axios'

const API_BASE_URL = 'http://localhost:5000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
})

export interface Report {
  date: string
  project_count: number
  content?: string  // 可选，用于详情页
}

export interface ReportContent {
  mdContent: string
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
  most_frequent_projects: [string, number][]
  most_frequent_languages: [string, number][]
  surging_projects: {
    name: string
    star_increase: number
    start_stars: number
    end_stars: number
  }[]
}

export const reportApi = {
  // 获取报告列表
  async getReports(): Promise<Report[]> {
    const response = await api.get('/api/reports')
    return response.data
  },

  // 获取具体报告内容
  async getReportContent(date: string): Promise<Report> {
    const response = await api.get(`/api/report/${date}`)
    return response.data
  },

  // 获取统计数据
  async getStats(): Promise<Stats> {
    const response = await api.get('/api/stats')
    return response.data
  },

  // 获取趋势数据
  async getTrends(): Promise<TrendsData> {
    const response = await api.get('/api/trends')
    return response.data
  },
}

// 导出便利函数
export const getReports = reportApi.getReports
export const getReportByDate = reportApi.getReportContent
export const getStats = reportApi.getStats
export const getTrends = reportApi.getTrends

export default api