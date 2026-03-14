const isObject = (v: unknown): v is Record<string, unknown> =>
  v !== null && typeof v === 'object' && !Array.isArray(v)

const snakeToCamel = (s: string) =>
  s.replace(/_([a-z])/g, (_, c) => c.toUpperCase())

const camelToSnake = (s: string) =>
  s.replace(/[A-Z]/g, c => '_' + c.toLowerCase())

export const camelizeKeys = (data: unknown): unknown => {
  if (Array.isArray(data)) return data.map(camelizeKeys)
  if (!isObject(data)) return data

  return Object.fromEntries(
    Object.entries(data).map(([k, v]) => [
      snakeToCamel(k),
      camelizeKeys(v)
    ])
  )
}

export const snakifyKeys = (data: unknown): unknown => {
  if (Array.isArray(data)) return data.map(snakifyKeys)
  if (!isObject(data)) return data

  return Object.fromEntries(
    Object.entries(data).map(([k, v]) => [
      camelToSnake(k),
      snakifyKeys(v)
    ])
  )
}
