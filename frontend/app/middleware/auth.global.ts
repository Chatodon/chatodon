export default defineNuxtRouteMiddleware(async (to, _) => {
  const router = useRouter()
  const account = useAccount()
  const me = await account.getMe()

  if (me) {
    if (to.name === 'login') {
      router.replace('/')
    }
  } else {
    if (to.name !== 'login') {
      router.replace('/login')
    }
  }
})
