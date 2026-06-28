'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useAuth } from '@/lib/hooks/use-auth'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { AlertCircle } from 'lucide-react'
import { useTranslation } from '@/lib/hooks/use-translation'

export function RegisterForm() {
  const { t } = useTranslation()
  const { register, isLoading, error } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [name, setName] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (email.trim() && password.length >= 6) {
      await register(email.trim(), password, name.trim() || undefined)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle>{t('auth.registerTitle', { defaultValue: 'Create account' })}</CardTitle>
          <CardDescription>
            {t('auth.registerDesc', { defaultValue: 'Sign up to start using your knowledge base.' })}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="name">{t('auth.name', { defaultValue: 'Name (optional)' })}</Label>
              <Input
                id="name"
                type="text"
                autoComplete="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                disabled={isLoading}
              />
            </div>
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
            <div className="space-y-2">
              <Label htmlFor="password">
                {t('auth.password', { defaultValue: 'Password' })}
                <span className="text-xs text-muted-foreground ml-2">
                  ({t('auth.minChars', { defaultValue: 'min 6 chars' })})
                </span>
              </Label>
              <Input
                id="password"
                type="password"
                autoComplete="new-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={isLoading}
                required
                minLength={6}
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
              disabled={isLoading || !email.trim() || password.length < 6}
            >
              {isLoading ? t('auth.registering', { defaultValue: 'Creating…' }) : t('auth.register', { defaultValue: 'Register' })}
            </Button>

            <div className="text-center text-sm text-muted-foreground pt-2">
              {t('auth.haveAccount', { defaultValue: 'Already have an account?' })}{' '}
              <Link href="/login" className="text-primary underline-offset-4 hover:underline">
                {t('auth.signIn', { defaultValue: 'Sign in' })}
              </Link>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
