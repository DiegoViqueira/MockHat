

export interface Grammar {
    errors: GrammarError[]
}

export interface GrammarError {
    error_text: string
    corrected_text: string
    correction_explanation: string
}