import { Component, computed, effect, inject, input } from '@angular/core';
import { Router } from '@angular/router';
import { Class } from '../../../classes/models/class.model';
import { Assessment } from '../../models/assessment.model';
import { AssessmentStore } from '../../stores/assessment.store';
import { Writing } from '../../models/writing.model';
import { AppRoutes } from '../../../../@core/auth/models/routes.enum';
import { WritingPdfGeneratorService } from '../../services/writing-pdf-generator.service';
import { ClassStore } from '../../../classes/stores/class.store';

@Component({
  selector: 'wlk-assessment-writing-view',
  templateUrl: './assessment-writing-view.component.html',
  styleUrl: './assessment-writing-view.component.scss',
  standalone: false,
})
export class AssessmentWritingViewComponent {
  router = inject(Router);
  writingPdfGenerator = inject(WritingPdfGeneratorService);
  displayedColumns: string[] = ['name', 'status', 'score', 'percentage', 'review', 'download'];
  store = inject(AssessmentStore);
  classStore = inject(ClassStore);
  assessment = computed(() => this.store.assessment());
  class = computed(() => this.classStore.class());

  writings = computed(() => this.store.writings());

  getStudentName(studentId: string) {
    const student = this.class().students.find((student) => student._id === studentId);
    if (!student) {
      return '';
    }
    return student.name + ' ' + student.last_name;
  }

  getScore(writing: Writing) {
    return writing.ai_feedback.criterias.map((criteria) => criteria.score).reduce((a, b) => a + b, 0);
  }

  getPercentage(writing: Writing) {
    return (this.getScore(writing) / this.getMaxScore(writing)) * 100;
  }

  maxScoreIsValid(writing: Writing) {
    return writing.ai_feedback.criterias.every((criteria) => criteria.max_score !== null);
  }

  getMaxScore(writing: Writing) {
    return writing.ai_feedback.criterias.map((criteria) => criteria.max_score || 0).reduce((a, b) => a + b, 0);
  }

  downloadPdf(writing: Writing) {
    this.writingPdfGenerator.generatePdf(writing, this.assessment(), this.class());
  }

  openWritingReviewDialog(writing: Writing) {
    this.router.navigate([AppRoutes.Modules, AppRoutes.Assessments, AppRoutes.AssessmentWritingDetails], { queryParams: { writingId: writing.id } });
  }

  constructor() {
    effect(() => {
      if (this.assessment) {
        this.store.getAssessmentWritings(this.assessment()._id);
      }
    });
  }
}
