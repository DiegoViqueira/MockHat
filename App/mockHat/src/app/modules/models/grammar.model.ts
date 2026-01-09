import { ExamType } from "./exam_type.enum";
import { Institution } from "./institutions.enum";
import { TokensUsage } from "./tokens.model";
import { Level } from "./user-level.enum";

export interface GrammarError {
  text?: string;
  corrected_text?: string;
  correction_explanation?: string;
}

export interface GrammarImprovementArea {
  area?: string;
  feedback?: string;
}

export interface Grammar {
  _id: string;
  user_id?: string;
  student_id?: string;
  text?: string;
  errors?: [GrammarError];
  improvements_areas?: [GrammarImprovementArea];
  spent_tokens: TokensUsage;
  level?: Level;
  institution?: Institution;
  exam_type?: ExamType;
  rating: number;
  created_at: Date;
  updated_at: Date;
}
