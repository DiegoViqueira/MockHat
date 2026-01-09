import { Level } from '../../users/models/user-level.enum';
import { WritingState } from './writing.state.model';
import { Institution } from '../../shared/models/institutions.enum';
import { ExamType } from '../../shared/models/exam_type.enum';
import { TokensUsage } from '../../shared/models/tokens.model';
import { WritingTask } from './writing.task.model';
import { Grammar } from './grammar.model';
import { Student } from '../../students/models/student.model';
import { User } from '../../users/models/user.model';


export interface WritingCriteriaScore {
  criteria: string
  score: number
  max_score?: number
  feedback: string
}

export interface WritingAIFeedback {
  criterias: WritingCriteriaScore[]
  spent_tokens: TokensUsage
}



export interface Writing {
  id: string
  assessment_id: string
  class_id: string
  student: Student
  account_id: string
  user: User
  level: Level
  institution: Institution
  exam_type: ExamType
  task: WritingTask
  student_response_image_urls: string[]
  student_response_text: string
  student_response_word_count: number
  student_response_tokens_usage: TokensUsage
  grammar_feedback: Grammar
  grammar_feedback_tokens_usage: TokensUsage
  ai_feedback: WritingAIFeedback
  writing_state: WritingState
  error_message: string
  writing_score: number
  created_at: Date
  updated_at: Date
}
