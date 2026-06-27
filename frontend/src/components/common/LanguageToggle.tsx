'use client'

import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { Languages } from 'lucide-react'
import { languages, normalizeLanguageCode } from '@/lib/locales'
import { useTranslation } from '@/lib/hooks/use-translation'

interface LanguageToggleProps {
  iconOnly?: boolean
}

export function LanguageToggle({ iconOnly = false }: LanguageToggleProps) {
  const { language, setLanguage, t } = useTranslation()
  const currentLang = normalizeLanguageCode(language)

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          variant={iconOnly ? 'ghost' : 'outline'}
          size={iconOnly ? 'icon' : 'default'}
          className={iconOnly ? 'h-9 w-full sidebar-menu-item' : 'w-full justify-start gap-2 sidebar-menu-item'}
        >
          <Languages className="h-[1.2rem] w-[1.2rem]" />
          {!iconOnly && <span>{t('common.language')}</span>}
          <span className="sr-only">{t('navigation.language')}</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        {languages.map((candidate) => (
          <DropdownMenuItem
            key={candidate.code}
            onClick={() => setLanguage(candidate.code)}
            className={currentLang === candidate.code ? 'bg-accent' : ''}
          >
            <span>{candidate.label}</span>
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
