import { AssessmentState } from "./assessment.state.model"
import { ExamType } from "../../shared/models/exam_type.enum"
import { Institution } from "../../shared/models/institutions.enum"
import { TokensUsage } from "../../shared/models/tokens.model"
import { Level } from "../../users/models/user-level.enum"
import { WritingTask } from "./writing.task.model"


export interface Assessment {
    _id: string,
    account_id: string
    class_id: string
    user_id: string
    level: Level
    institution: Institution
    exam_type: ExamType
    task: WritingTask
    title: string
    description: string
    image_url: string
    image_text: string
    image_transcription_tokens_usage: TokensUsage
    state: AssessmentState
    created_at: Date
    updated_at: Date
}