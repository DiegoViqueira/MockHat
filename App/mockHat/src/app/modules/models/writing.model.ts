import { ExamType } from "./exam_type.enum";
import { Institution } from "./institutions.enum";
import { TokensUsage } from "./tokens.model";
import { Level } from "./user-level.enum";
import { WritingAiResponse } from "./writing.ai.response.model";
import { WritingState } from "./writing.state.model";

export interface Writing {
  _id: string;
  task?: string;
  student_id?: string;
  text_question?: string;
  spent_tokens_question: TokensUsage;
  text_response?: string;
  spent_tokens_response: TokensUsage;
  ai_response?: WritingAiResponse;
  user_id?: string;
  level: Level;
  institution?: Institution;
  exam_type?: ExamType;
  state: WritingState;
  rating: number;
  created_at: Date;
  updated_at: Date;
}
