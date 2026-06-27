import { zhCN } from './zh-CN'
import { enUS } from './en-US'
import { zhTW } from './zh-TW'
import { ptBR } from './pt-BR'
import { jaJP } from './ja-JP'
import { itIT } from './it-IT'
import { frFR } from './fr-FR'
import { ruRU } from './ru-RU'
import { bnIN } from './bn-IN'
import { caES } from './ca-ES'
import { esES } from './es-ES'
import { deDE } from './de-DE'
import { plPL } from './pl-PL'
import { trTR } from './tr-TR'
import { viVN } from './vi-VN'
import { enSG } from './en-SG'
import { zhSG } from './zh-SG'
import { koKR } from './ko-KR'
import { hiIN } from './hi-IN'
import { idID } from './id-ID'
import { thTH } from './th-TH'
import { arSA } from './ar-SA'
import { nlNL } from './nl-NL'
import { svSE } from './sv-SE'
import { nbNO } from './nb-NO'
import { daDK } from './da-DK'
import { fiFI } from './fi-FI'
import { elGR } from './el-GR'
import { heIL } from './he-IL'
import { csCZ } from './cs-CZ'
import { huHU } from './hu-HU'
import { roRO } from './ro-RO'
import { ukUA } from './uk-UA'
import { msMY } from './ms-MY'
import { faIR } from './fa-IR'

export const resources = {
  'zh-CN': { translation: zhCN },
  'en-US': { translation: enUS },
  'zh-TW': { translation: zhTW },
  'pt-BR': { translation: ptBR },
  'ja-JP': { translation: jaJP },
  'it-IT': { translation: itIT },
  'fr-FR': { translation: frFR },
  'ru-RU': { translation: ruRU },
  'bn-IN': { translation: bnIN },
  'ca-ES': { translation: caES },
  'es-ES': { translation: esES },
  'de-DE': { translation: deDE },
  'pl-PL': { translation: plPL },
  'tr-TR': { translation: trTR },
  'vi-VN': { translation: viVN },
  'en-SG': { translation: enSG },
  'zh-SG': { translation: zhSG },
  'ko-KR': { translation: koKR },
  'hi-IN': { translation: hiIN },
  'id-ID': { translation: idID },
  'th-TH': { translation: thTH },
  'ar-SA': { translation: arSA },
  'nl-NL': { translation: nlNL },
  'sv-SE': { translation: svSE },
  'nb-NO': { translation: nbNO },
  'da-DK': { translation: daDK },
  'fi-FI': { translation: fiFI },
  'el-GR': { translation: elGR },
  'he-IL': { translation: heIL },
  'cs-CZ': { translation: csCZ },
  'hu-HU': { translation: huHU },
  'ro-RO': { translation: roRO },
  'uk-UA': { translation: ukUA },
  'ms-MY': { translation: msMY },
  'fa-IR': { translation: faIR },
} as const

export type TranslationKeys = typeof enUS
export type LanguageCode = keyof typeof resources

export type Language = {
  code: LanguageCode
  label: string
  aliases?: string[]
  fallback?: LanguageCode
}

export const languageFallbacks: Partial<Record<LanguageCode, LanguageCode>> = {
  'en-SG': 'en-US',
  'zh-SG': 'zh-CN',
}

export const languages: Language[] = [
  { code: 'en-US', label: 'English', aliases: ['en'] },
  { code: 'en-SG', label: 'English (Singapore)' },
  { code: 'ca-ES', label: 'Català', aliases: ['ca'] },
  { code: 'zh-CN', label: '简体中文', aliases: ['zh', 'zh-Hans'] },
  { code: 'zh-SG', label: '简体中文（新加坡）' },
  { code: 'zh-TW', label: '繁體中文', aliases: ['zh-Hant'] },
  { code: 'vi-VN', label: 'Tiếng Việt', aliases: ['vi'] },
  { code: 'pt-BR', label: 'Português (Brasil)', aliases: ['pt'] },
  { code: 'ja-JP', label: '日本語', aliases: ['ja'] },
  { code: 'ko-KR', label: '한국어', aliases: ['ko'] },
  { code: 'hi-IN', label: 'हिन्दी', aliases: ['hi'] },
  { code: 'id-ID', label: 'Bahasa Indonesia', aliases: ['id'] },
  { code: 'th-TH', label: 'ไทย', aliases: ['th'] },
  { code: 'ar-SA', label: 'العربية', aliases: ['ar'] },
  { code: 'fa-IR', label: 'فارسی', aliases: ['fa'] },
  { code: 'he-IL', label: 'עברית', aliases: ['he'] },
  { code: 'ms-MY', label: 'Bahasa Melayu', aliases: ['ms'] },
  { code: 'nl-NL', label: 'Nederlands', aliases: ['nl'] },
  { code: 'sv-SE', label: 'Svenska', aliases: ['sv'] },
  { code: 'nb-NO', label: 'Norsk bokmål', aliases: ['nb', 'no'] },
  { code: 'da-DK', label: 'Dansk', aliases: ['da'] },
  { code: 'fi-FI', label: 'Suomi', aliases: ['fi'] },
  { code: 'el-GR', label: 'Ελληνικά', aliases: ['el'] },
  { code: 'cs-CZ', label: 'Čeština', aliases: ['cs'] },
  { code: 'hu-HU', label: 'Magyar', aliases: ['hu'] },
  { code: 'ro-RO', label: 'Română', aliases: ['ro'] },
  { code: 'uk-UA', label: 'Українська', aliases: ['uk'] },
  { code: 'it-IT', label: 'Italiano', aliases: ['it'] },
  { code: 'fr-FR', label: 'Français', aliases: ['fr'] },
  { code: 'ru-RU', label: 'Русский', aliases: ['ru'] },
  { code: 'bn-IN', label: 'বাংলা', aliases: ['bn'] },
  { code: 'es-ES', label: 'Español', aliases: ['es'] },
  { code: 'de-DE', label: 'Deutsch', aliases: ['de'] },
  { code: 'pl-PL', label: 'Polski', aliases: ['pl'] },
  { code: 'tr-TR', label: 'Türkçe', aliases: ['tr'] },
]

const supportedLanguageCodes = new Set<LanguageCode>(
  languages.map((language) => language.code),
)

export function normalizeLanguageCode(language?: string | null): LanguageCode {
  if (!language) {
    return 'en-US'
  }

  if (supportedLanguageCodes.has(language as LanguageCode)) {
    return language as LanguageCode
  }

  const matchedLanguage = languages.find((candidate) =>
    candidate.aliases?.some((alias) => language === alias || language.startsWith(`${alias}-`)),
  )

  return matchedLanguage?.code ?? 'en-US'
}

export { zhCN, enUS, zhTW, ptBR, jaJP, itIT, frFR, ruRU, bnIN, caES, esES, deDE, plPL, trTR, viVN, enSG, zhSG, koKR, hiIN, idID, thTH, arSA, nlNL, svSE, nbNO, daDK, fiFI, elGR, heIL, csCZ, huHU, roRO, ukUA, msMY, faIR }
