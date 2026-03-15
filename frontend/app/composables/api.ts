export interface ApiResponse extends Response {
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

    if (!isFormData && options.body && typeof options.body === 'string') {
      headers.set('Content-Type', 'application/json')
    }

    try {
      const res = await fetch(`${config.public.apiBase}${url}`, {
        ...options,
        headers,
        credentials: 'include'
      })

      const apiRes = res as ApiResponse

      if (apiRes.headers.get('content-type')?.includes('application/json')) {
        apiRes.data = await res.clone().json()
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
