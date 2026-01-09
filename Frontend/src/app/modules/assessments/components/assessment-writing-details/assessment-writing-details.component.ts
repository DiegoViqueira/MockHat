import { Component, inject, computed, effect, OnChanges } from '@angular/core';
import { AssessmentStore } from '../../stores/assessment.store';
import { ActivatedRoute } from '@angular/router';
import { WritingAIFeedback } from '../../models/writing.model';
import { GrammarError } from '../../models/grammar.model';
@Component({
  selector: 'wlk-assessment-writing-details',
  templateUrl: './assessment-writing-details.component.html',
  styleUrl: './assessment-writing-details.component.scss',
  standalone: false,
})
export class AssessmentWritingDetailsComponent implements OnChanges {
  route = inject(ActivatedRoute);

  grammarErrors: GrammarError[] = [];
  assessmentStore = inject(AssessmentStore);
  assessment = computed(() => this.assessmentStore.assessment());
  writings = computed(() => this.assessmentStore.writings());
  writingId = this.route.snapshot.queryParams['writingId'];
  writing = undefined;
  isSidenavOpen = true;

  highlightedError: GrammarError | null = null;


  openTooltip(error: GrammarError) {
    this.highlightedError = error;
  }

  constructor() {
    effect(() => {
      if (this.writings()) {
        this.writing = this.writings().find((writing) => writing.id === this.writingId);
        this.grammarErrors = this.writing?.grammar_feedback.errors;

      }
    });
  }

  ngOnChanges(): void {
    this.grammarErrors = this.writing?.grammar_feedback.errors;
  }

  calculateScore(aiFeedback: WritingAIFeedback) {
    return aiFeedback.criterias.map((criteria) => criteria.score).reduce((a, b) => a + b, 0);
  }

  calculateMaxScore(aiFeedback: WritingAIFeedback) {
    return aiFeedback.criterias
      .map((criteria) => criteria.max_score || 0)
      .reduce((a, b) => a + b, 0);
  }


  updateAIFeedback() {
    const aiFeedback = this.writing?.ai_feedback;
    this.assessmentStore.updateWritingAIFeedback(this.assessment()._id, this.writing?.id, aiFeedback);
  }

  removeError(error: GrammarError) {
    this.assessmentStore.updateAssessmentGrammarFeedback(this.assessment()._id, this.writing?.id, {
      ...this.writing?.grammar_feedback,
      errors: this.grammarErrors.filter((e) => e.error_text !== error.error_text),
    });
  }
}
