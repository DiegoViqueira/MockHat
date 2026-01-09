import { ImageFile } from './image.file.model';
import { WritingAssessmentItemState } from './writing.assessment.item.state.model';
import { Writing } from './writing.model';

export interface WritingAssessmentItem {
  student_id?: string;
  student_name?: string;
  file?: ImageFile;
  state?: WritingAssessmentItemState;
  writing?: Writing;
}
