import { TokensUsage } from "./tokens.model";


export interface WritingCriteriaScore {
  criteria?: string;
  score?: number;
  feedback?: string;
}
export interface WritingAiResponse {
  criterias?: WritingCriteriaScore[];
  spent_tokens: TokensUsage;
}
