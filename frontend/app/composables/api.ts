import { camelizeKeys, snakifyKeys } from '~/utils/case'

export interface ApiResponse extends Response {
  jsonCamel<T = unknown>(): Promise<T | unknown>
  jsonSnake<T = unknown>(): Promise<T | unknown>
  data: unknown
}

const getCsrfToken = (): string | undefined => {
  const match = document.cookie.match(/csrftoken=([\w-]+)/)
  return match ? match[1] : ''
}

export const useApi = () => {
  const config = useRuntimeConfig()
  const error = ref<Error | null>(null)
  const loading = ref(false)

  const request = async (
    url: string,
    options: RequestInit = {}
  ): Promise<ApiResponse | null> => {
    loading.value = true
    error.value = null

    const headers = new Headers(options.headers)
    const csrf = getCsrfToken()
    if (csrf) headers.set('X-CSRFToken', csrf)
    const isFormData = options.body instanceof FormData

    // outgoing snake_case
    let body = options.body
    if (body && !isFormData && typeof body === 'string') {
      try {
        const parsed = JSON.parse(body)
        body = JSON.stringify(snakifyKeys(parsed))
        headers.set('Content-Type', 'application/json')
      } catch {
        // pass
      }
    }

    try {
      const res = await fetch(`${config.public.apiBase}${url}`, {
        ...options,
        headers,
        credentials: 'include'
      })

      // proxy Response
      const apiRes = res as ApiResponse

      apiRes.jsonSnake = async (): Promise<unknown> => {
        return res.clone().json()
      }

      apiRes.jsonCamel = async (): Promise<unknown> => {
        const data = await res.clone().json()
        return camelizeKeys(data)
      }

      if (apiRes.headers.get('content-type')?.includes('application/json')) {
        apiRes.data = await apiRes.jsonCamel()
      }

      return apiRes
    } catch (err: unknown) {
      error.value = err instanceof Error ? err : new Error('Unknown error')
      return null
    } finally {
      loading.value = false
    }
  }

  const get = (url: string) => request(url, { method: 'GET' })

  const post = (url: string, body: unknown) =>
    request(url, {
      method: 'POST',
      body: body instanceof FormData ? body : JSON.stringify(body)
    })

  const put = (url: string, body: unknown) =>
    request(url, {
      method: 'PUT',
      body: body instanceof FormData ? body : JSON.stringify(body)
    })

  const patch = (url: string, body: unknown) =>
    request(url, {
      method: 'PATCH',
      body: body instanceof FormData ? body : JSON.stringify(body)
    })

  const del = (url: string) => request(url, { method: 'DELETE' })

  return {
    error,
    loading,
    get,
    post,
    put,
    patch,
    del
  }
}
