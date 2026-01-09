import { effect, inject, Injectable, signal, WritableSignal } from '@angular/core';
import { WritingAssessmentItem } from '../models/writing.assessmen.item.model';
import { Level } from '../../users/models/user-level.enum';
import { WritingAssessmentItemState } from '../models/writing.assessment.item.state.model';
import { StudentsStore } from '../../students/stores/students.store';
import { ImageFile } from '../../../@shared/components/file-loader/file-loader.component';
import { Writing } from '../models/writing.model';

@Injectable({
  providedIn: 'root',
})
export class AssessmentCorrectionStoreService {
  public assessments: WritableSignal<WritingAssessmentItem[]> = signal(undefined);
  private level = signal(Level.B1);
  private store = inject(StudentsStore);

  constructor() {
    effect(
      () => {
        if (this.store.students() && this.store.students().length > 0) {
          this.selectByLevel(this.level());
        }
      },
      { allowSignalWrites: true }
    );
  }

  removeItem(student_id: string) {
    const currentAssessments = this.assessments();

    const updatedAssessments = currentAssessments.filter(
      (assessment) => assessment.student_id !== student_id
    );

    this.assessments.set(updatedAssessments);
  }

  updateState(student_id: string, state: WritingAssessmentItemState, writing: Writing) {
    const currentAssessments = this.assessments();

    const assessmentIndex = currentAssessments.findIndex((x) => x.student_id === student_id);

    if (assessmentIndex !== -1) {
      const updatedAssessment = {
        ...currentAssessments[assessmentIndex],
        state: state,
        writing: writing,
      };

      const updatedAssessments = [...currentAssessments];
      updatedAssessments[assessmentIndex] = updatedAssessment;

      this.assessments.set(updatedAssessments);
    } else {
      console.warn(`Assessment with student_id: ${student_id} not found.`);
    }
  }

  updateAssessmentFile(student_id: string, file: ImageFile) {
    const currentAssessments = this.assessments();

    const assessmentIndex = currentAssessments.findIndex((x) => x.student_id === student_id);

    if (assessmentIndex !== -1) {
      const updatedAssessment = {
        ...currentAssessments[assessmentIndex],
        file: file,
      };

      const updatedAssessments = [...currentAssessments];
      updatedAssessments[assessmentIndex] = updatedAssessment;

      this.assessments.set(updatedAssessments);
    } else {
      console.warn(`Assessment with student_id: ${student_id} not found.`);
    }
  }
  selectByLevel(level: Level) {
    this.level.set(level);
    /*  const filteredStudents = this.store.students().filter((x) => x.level === level);
      const filteredAssessments: WritingAssessmentItem[] = filteredStudents.map((student) => ({
        student_id: student.id,
        student_name: student.name + ' ' + student.last_name,
        file: undefined,
        state: WritingAssessmentItemState.Pending,
        writing: undefined,
      }));
      this.assessments.set(filteredAssessments);
      */
  }
}
