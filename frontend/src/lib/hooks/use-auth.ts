'use client'

import { useAuthStore } from '@/lib/stores/auth-store'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export function useAuth() {
  const router = useRouter()
  const {
    isAuthenticated,
    isLoading,
    login,
    register,
    loginWithPassword,
    logout,
    checkAuth,
    checkAuthRequired,
    error,
    hasHydrated,
    authRequired,
    authMode,
    user,
  } = useAuthStore()

  useEffect(() => {
    if (hasHydrated) {
      if (authRequired === null) {
        checkAuthRequired().then((required) => {
          if (required) {
            checkAuth()
          }
        })
      } else if (authRequired) {
        checkAuth()
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [hasHydrated, authRequired])

  const redirectAfterAuth = () => {
    const redirectPath = sessionStorage.getItem('redirectAfterLogin')
    if (redirectPath) {
      sessionStorage.removeItem('redirectAfterLogin')
      router.push(redirectPath)
    } else {
      router.push('/notebooks')
    }
  }

  // JWT (multi-tenant) login: email + password
  const handleLogin = async (email: string, password: string) => {
    const success = await login(email, password)
    if (success) redirectAfterAuth()
    return success
  }

  // JWT registration
  const handleRegister = async (email: string, password: string, name?: string) => {
    const success = await register(email, password, name)
    if (success) redirectAfterAuth()
    return success
  }

  // Legacy deployment-password login
  const handlePasswordLogin = async (password: string) => {
    const success = await loginWithPassword(password)
    if (success) redirectAfterAuth()
    return success
  }

  const handleLogout = () => {
    logout()
    router.push('/login')
  }

  return {
    isAuthenticated,
    isLoading: isLoading || !hasHydrated,
    error,
    authMode,
    user,
    login: handleLogin,
    register: handleRegister,
    loginWithPassword: handlePasswordLogin,
    logout: handleLogout,
  }
}
