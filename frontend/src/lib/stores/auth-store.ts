import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { getApiUrl } from '@/lib/config'

interface UserInfo {
  id: string
  email: string
  name: string | null
  tier: string | null
}

interface AuthState {
  isAuthenticated: boolean
  token: string | null
  user: UserInfo | null
  isLoading: boolean
  error: string | null
  lastAuthCheck: number | null
  isCheckingAuth: boolean
  hasHydrated: boolean
  // 'jwt' = multi-tenant (email+password), 'password' = legacy deployment
  // password, 'none' = no auth. null = not yet checked.
  authMode: 'jwt' | 'password' | 'none' | null
  // Backward-compat boolean: true if any auth is required.
  authRequired: boolean | null
  setHasHydrated: (state: boolean) => void
  checkAuthRequired: () => Promise<boolean>
  // JWT mode
  login: (email: string, password: string) => Promise<boolean>
  register: (email: string, password: string, name?: string) => Promise<boolean>
  // Legacy password mode (kept for backward compat)
  loginWithPassword: (password: string) => Promise<boolean>
  logout: () => void
  checkAuth: () => Promise<boolean>
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      isAuthenticated: false,
      token: null,
      user: null,
      isLoading: false,
      error: null,
      lastAuthCheck: null,
      isCheckingAuth: false,
      hasHydrated: false,
      authMode: null,
      authRequired: null,

      setHasHydrated: (state: boolean) => {
        set({ hasHydrated: state })
      },

      checkAuthRequired: async () => {
        try {
          const apiUrl = await getApiUrl()
          const response = await fetch(`${apiUrl}/api/auth/status`, {
            cache: 'no-store',
          })

          if (!response.ok) {
            throw new Error(`Auth status check failed: ${response.status}`)
          }

          const data = await response.json()
          const mode = (data.auth_mode || 'none') as 'jwt' | 'password' | 'none'
          const required = data.auth_enabled || false
          set({ authMode: mode, authRequired: required })

          // If auth is not required, mark as authenticated
          if (!required) {
            set({ isAuthenticated: true, token: 'not-required' })
          }

          return required
        } catch (error) {
          console.error('Failed to check auth status:', error)
          if (error instanceof TypeError && error.message.includes('Failed to fetch')) {
            set({
              error: 'Unable to connect to server. Please check if the API is running.',
              authMode: null,
            })
          } else {
            set({ authMode: 'none' })
          }
          throw error
        }
      },

      // --- JWT (multi-tenant) login ---

      login: async (email: string, password: string) => {
        set({ isLoading: true, error: null })
        try {
          const apiUrl = await getApiUrl()
          const response = await fetch(`${apiUrl}/api/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
          })

          if (response.ok) {
            const data = await response.json()
            set({
              isAuthenticated: true,
              token: data.token,
              user: data.user,
              isLoading: false,
              lastAuthCheck: Date.now(),
              error: null,
            })
            return true
          }

          const detail = await response.json().catch(() => ({}))
          let errorMessage = 'Authentication failed'
          if (response.status === 401) {
            errorMessage = detail.detail || 'Incorrect email or password.'
          } else if (response.status === 400) {
            errorMessage = detail.detail || 'User login is not enabled on this server.'
          } else if (response.status >= 500) {
            errorMessage = 'Server error. Please try again later.'
          }
          set({ error: errorMessage, isLoading: false, isAuthenticated: false, token: null })
          return false
        } catch (error) {
          console.error('Network error during login:', error)
          set({
            error: error instanceof TypeError && error.message.includes('Failed to fetch')
              ? 'Unable to connect to server. Please check if the API is running.'
              : 'Network error during login.',
            isLoading: false,
            isAuthenticated: false,
            token: null,
          })
          return false
        }
      },

      register: async (email: string, password: string, name?: string) => {
        set({ isLoading: true, error: null })
        try {
          const apiUrl = await getApiUrl()
          const response = await fetch(`${apiUrl}/api/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password, name }),
          })

          if (response.ok) {
            const data = await response.json()
            set({
              isAuthenticated: true,
              token: data.token,
              user: data.user,
              isLoading: false,
              lastAuthCheck: Date.now(),
              error: null,
            })
            return true
          }

          const detail = await response.json().catch(() => ({}))
          let errorMessage = 'Registration failed'
          if (response.status === 409) {
            errorMessage = 'This email is already registered.'
          } else if (response.status === 400) {
            errorMessage = detail.detail || 'Registration is not enabled on this server.'
          }
          set({ error: errorMessage, isLoading: false })
          return false
        } catch (error) {
          console.error('Network error during register:', error)
          set({
            error: 'Network error during registration.',
            isLoading: false,
          })
          return false
        }
      },

      // --- Legacy deployment-password login (kept for backward compat) ---

      loginWithPassword: async (password: string) => {
        set({ isLoading: true, error: null })
        try {
          const apiUrl = await getApiUrl()
          const response = await fetch(`${apiUrl}/api/notebooks`, {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${password}`,
              'Content-Type': 'application/json',
            },
          })

          if (response.ok) {
            set({
              isAuthenticated: true,
              token: password,
              user: null,
              isLoading: false,
              lastAuthCheck: Date.now(),
              error: null,
            })
            return true
          }

          let errorMessage = 'Authentication failed'
          if (response.status === 401) errorMessage = 'Invalid password. Please try again.'
          else if (response.status >= 500) errorMessage = 'Server error. Please try again later.'
          set({ error: errorMessage, isLoading: false, isAuthenticated: false, token: null })
          return false
        } catch (error) {
          console.error('Network error during auth:', error)
          set({
            error: error instanceof TypeError && error.message.includes('Failed to fetch')
              ? 'Unable to connect to server. Please check if the API is running.'
              : 'Network error.',
            isLoading: false,
            isAuthenticated: false,
            token: null,
          })
          return false
        }
      },

      logout: () => {
        set({ isAuthenticated: false, token: null, user: null, error: null })
      },

      checkAuth: async () => {
        const state = get()
        const { token, lastAuthCheck, isCheckingAuth, isAuthenticated } = state

        if (isCheckingAuth) return isAuthenticated
        if (!token || token === 'not-required') return token === 'not-required'

        const now = Date.now()
        if (isAuthenticated && lastAuthCheck && now - lastAuthCheck < 30000) {
          return true
        }

        set({ isCheckingAuth: true })
        try {
          const apiUrl = await getApiUrl()
          const response = await fetch(`${apiUrl}/api/notebooks`, {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
          })

          if (response.ok) {
            set({ isAuthenticated: true, lastAuthCheck: now, isCheckingAuth: false })
            return true
          }
          set({
            isAuthenticated: false,
            token: null,
            user: null,
            lastAuthCheck: null,
            isCheckingAuth: false,
          })
          return false
        } catch (error) {
          console.error('checkAuth error:', error)
          set({
            isAuthenticated: false,
            token: null,
            user: null,
            lastAuthCheck: null,
            isCheckingAuth: false,
          })
          return false
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        token: state.token,
        isAuthenticated: state.isAuthenticated,
        user: state.user,
        authMode: state.authMode,
        authRequired: state.authRequired,
      }),
      onRehydrateStorage: () => (state) => {
        state?.setHasHydrated(true)
      },
    },
  ),
)
