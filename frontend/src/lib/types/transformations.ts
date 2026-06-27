export interface TransformationTranslation {
  name?: string
  title?: string
  description?: string
  prompt?: string
}

export interface DefaultPromptTranslation {
  transformation_instructions?: string
}

export interface Transformation {
  id: string
  name: string
  title: string
  description: string
  prompt: string
  apply_default: boolean
  source_locale: string
  system_key?: string | null
  translations?: Record<string, TransformationTranslation>
  created: string
  updated: string
}

export interface CreateTransformationRequest {
  name: string
  title: string
  description: string
  prompt: string
  apply_default?: boolean
  source_locale: string
  system_key?: string | null
  translations?: Record<string, TransformationTranslation>
}

export interface UpdateTransformationRequest {
  name?: string
  title?: string
  description?: string
  prompt?: string
  apply_default?: boolean
  source_locale?: string
  system_key?: string | null
  translations?: Record<string, TransformationTranslation>
}

export interface ExecuteTransformationRequest {
  transformation_id: string
  input_text: string
  model_id: string
  locale: string
}

export interface ExecuteTransformationResponse {
  output: string
  transformation_id: string
  model_id: string
}

export interface DefaultPrompt {
  transformation_instructions: string
  source_locale: string
  translations: Record<string, DefaultPromptTranslation>
}
