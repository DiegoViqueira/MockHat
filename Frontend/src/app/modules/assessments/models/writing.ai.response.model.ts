import { TokensUsage } from '../../shared/models/tokens.model';

export interface WritingCriteriaScore {
  criteria?: string;
  score?: number;
  feedback?: string;
}
export interface WritingAiResponse {
  criterias?: WritingCriteriaScore[];
  spent_tokens: TokensUsage;
}


export interface TranscribeAiResponse {
  text: string;
}


