import { languageFallbacks, normalizeLanguageCode } from '@/lib/locales'
import {
  DefaultPrompt,
  DefaultPromptTranslation,
  Transformation,
  TransformationTranslation,
} from '@/lib/types/transformations'

const DEFAULT_LOCALE = 'en-US'

type TranslationMap<T> = Record<string, T> | undefined

const hasText = (value?: string | null): value is string =>
  typeof value === 'string' && value.trim() !== ''

export function getLocaleCandidates(locale?: string, sourceLocale?: string): string[] {
  const currentLocale = normalizeLanguageCode(locale)
  const candidates = [currentLocale]
  const fallbackLocale = languageFallbacks[currentLocale]

  if (fallbackLocale && !candidates.includes(fallbackLocale)) {
    candidates.push(fallbackLocale)
  }

  const normalizedSourceLocale = normalizeLanguageCode(sourceLocale)
  if (!candidates.includes(normalizedSourceLocale)) {
    candidates.push(normalizedSourceLocale)
  }

  if (!candidates.includes(DEFAULT_LOCALE)) {
    candidates.push(DEFAULT_LOCALE)
  }

  return candidates
}

function resolveField<T extends object>(
  translations: TranslationMap<T>,
  locale: string | undefined,
  sourceLocale: string | undefined,
  field: keyof T,
  fallbackValue: string,
): string {
  for (const candidate of getLocaleCandidates(locale, sourceLocale)) {
    const entry = translations?.[candidate] as T | undefined
    if (!entry) continue
    const value = (entry as Record<string, unknown>)[field as string]
    if (hasText(value as string | null | undefined)) {
      return value as string
    }
  }

  return fallbackValue
}

export function resolveTransformationFields(
  transformation: Pick<Transformation, 'name' | 'title' | 'description' | 'prompt' | 'source_locale' | 'translations'>,
  locale?: string,
): { name: string; title: string; description: string; prompt: string } {
  const translations = transformation.translations as TranslationMap<TransformationTranslation>

  return {
    name: resolveField(translations, locale, transformation.source_locale, 'name', transformation.name),
    title: resolveField(translations, locale, transformation.source_locale, 'title', transformation.title || transformation.name),
    description: resolveField(translations, locale, transformation.source_locale, 'description', transformation.description || ''),
    prompt: resolveField(translations, locale, transformation.source_locale, 'prompt', transformation.prompt),
  }
}

export function resolveDefaultPromptInstructions(
  defaultPrompt: Pick<DefaultPrompt, 'transformation_instructions' | 'source_locale' | 'translations'>,
  locale?: string,
): string {
  return resolveField(
    defaultPrompt.translations as TranslationMap<DefaultPromptTranslation>,
    locale,
    defaultPrompt.source_locale,
    'transformation_instructions',
    defaultPrompt.transformation_instructions || '',
  )
}

export function toTransformationTranslation(
  fields: { name: string; title: string; description: string; prompt: string },
): TransformationTranslation {
  return {
    name: fields.name,
    title: fields.title,
    description: fields.description,
    prompt: fields.prompt,
  }
}
