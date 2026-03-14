export interface PaginatedResponse {
  next: string | null
  previous: string | null
  count: number
  results: Array[unknown]
}
