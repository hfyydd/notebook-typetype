import { arSA, bn, ca, cs, da, de, el, enUS, es, faIR, fi, fr, he, hi, hu, id, it, ja, ko, Locale, ms, nb, nl, pl, ptBR, ro, ru, sv, th, tr, uk, vi, zhCN, zhTW } from 'date-fns/locale'

import { normalizeLanguageCode } from '@/lib/locales'

const LOCALE_MAP: Record<string, Locale> = {
  'zh-CN': zhCN,
  'zh-SG': zhCN,
  'zh-TW': zhTW,
  'en-US': enUS,
  'en-SG': enUS,
  'pt-BR': ptBR,
  'ja-JP': ja,
  'ko-KR': ko,
  'hi-IN': hi,
  'id-ID': id,
  'th-TH': th,
  'ar-SA': arSA,
  'fa-IR': faIR,
  'he-IL': he,
  'ms-MY': ms,
  'nl-NL': nl,
  'sv-SE': sv,
  'nb-NO': nb,
  'da-DK': da,
  'fi-FI': fi,
  'el-GR': el,
  'cs-CZ': cs,
  'hu-HU': hu,
  'ro-RO': ro,
  'uk-UA': uk,
  'fr-FR': fr,
  'ru-RU': ru,
  'bn-IN': bn,
  'ca-ES': ca,
  'es-ES': es,
  'de-DE': de,
  'pl-PL': pl,
  'tr-TR': tr,
  'vi-VN': vi,
  'it-IT': it,
}

export function getDateLocale(language: string): Locale {
  return LOCALE_MAP[normalizeLanguageCode(language)] || enUS
}
