'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useAuth } from '@/lib/hooks/use-auth'
import { useAuthStore } from '@/lib/stores/auth-store'
import { getConfig } from '@/lib/config'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { AlertCircle } from 'lucide-react'
import { LoadingSpinner } from '@/components/common/LoadingSpinner'
import { useTranslation } from '@/lib/hooks/use-translation'

export function LoginForm() {
  const { t, language } = useTranslation()
  const { login, loginWithPassword, isLoading, error } = useAuth()
  const { authRequired, authMode, checkAuthRequired, hasHydrated, isAuthenticated } = useAuthStore()
  const [isCheckingAuth, setIsCheckingAuth] = useState(true)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [configInfo, setConfigInfo] = useState<{ apiUrl: string; version: string; buildTime: string } | null>(null)
  const router = useRouter()

  useEffect(() => {
    getConfig().then(cfg => {
      setConfigInfo({ apiUrl: cfg.apiUrl, version: cfg.version, buildTime: cfg.buildTime })
    }).catch(() => {})
  }, [])

  useEffect(() => {
    if (!hasHydrated) return
    const check = async () => {
      try {
        const required = await checkAuthRequired()
        if (!required) router.push('/notebooks')
      } catch {
        // keep showing form on error
      } finally {
        setIsCheckingAuth(false)
      }
    }
    if (authRequired !== null) {
      if (!authRequired && isAuthenticated) router.push('/notebooks')
      else setIsCheckingAuth(false)
    } else {
      void check()
    }
  }, [hasHydrated, authRequired, checkAuthRequired, router, isAuthenticated])

  if (!hasHydrated || isCheckingAuth) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <LoadingSpinner />
      </div>
    )
  }

  if (authRequired === null) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background p-4">
        <Card className="w-full max-w-md">
          <CardHeader className="text-center">
            <CardTitle>{t('common.connectionError')}</CardTitle>
            <CardDescription>{t('common.unableToConnect')}</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-start gap-2 text-red-600 text-sm">
              <AlertCircle className="h-4 w-4 mt-0.5 flex-shrink-0" />
              <div className="flex-1">{error || t('auth.connectErrorHint')}</div>
            </div>
            {configInfo && (
              <div className="space-y-1 text-xs text-muted-foreground border-t pt-3 mt-3 font-mono">
                <div>{t('common.version')}: {configInfo.version}</div>
                <div className="break-all">{t('common.apiUrl')}: {configInfo.apiUrl}</div>
              </div>
            )}
            <Button onClick={() => window.location.reload()} className="w-full mt-4">
              {t('common.retryConnection')}
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  // --- JWT mode: email + password + link to register ---
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (authMode === 'jwt') {
      if (email.trim() && password) await login(email.trim(), password)
    } else {
      // legacy password mode
      if (password.trim()) await loginWithPassword(password)
    }
  }

  const isJwt = authMode === 'jwt'

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle>{t('auth.loginTitle')}</CardTitle>
          <CardDescription>{t('auth.loginDesc')}</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {isJwt && (
              <div className="space-y-2">
                <Label htmlFor="email">{t('auth.email', { defaultValue: 'Email' })}</Label>
                <Input
                  id="email"
                  type="email"
                  autoComplete="email"
                  placeholder="you@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  disabled={isLoading}
                  required
                />
              </div>
            )}
            <div className="space-y-2">
              {isJwt && (
                <Label htmlFor="password">{t('auth.password', { defaultValue: 'Password' })}</Label>
              )}
              <Input
                id="password"
                type="password"
                autoComplete={isJwt ? 'current-password' : 'off'}
                placeholder={isJwt ? '' : t('auth.passwordPlaceholder')}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={isLoading}
                required
              />
            </div>

            {error && (
              <div className="flex items-center gap-2 text-red-600 text-sm">
                <AlertCircle className="h-4 w-4" />
                {error}
              </div>
            )}

            <Button
              type="submit"
              className="w-full"
              disabled={isLoading || (!isJwt ? !password.trim() : !email.trim() || !password)}
            >
              {isLoading ? t('auth.signingIn') : t('auth.signIn')}
            </Button>

            {isJwt && (
              <div className="text-center text-sm text-muted-foreground pt-2">
                {t('auth.noAccount', { defaultValue: 'No account?' })}{' '}
                <Link href="/register" className="text-primary underline-offset-4 hover:underline">
                  {t('auth.register', { defaultValue: 'Register' })}
                </Link>
              </div>
            )}

            {configInfo && (
              <div className="text-xs text-center text-muted-foreground pt-2 border-t">
                <div>{t('common.version')} {configInfo.version}</div>
              </div>
            )}
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
