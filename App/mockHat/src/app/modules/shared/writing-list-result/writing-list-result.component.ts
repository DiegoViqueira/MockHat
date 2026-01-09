import { Component, effect, inject, OnInit } from '@angular/core';
import { WritingAssessmentItem } from '../../models/writing.assessmen.item.model';
import { AssessmentCorrectionStoreService } from '../../stores/assesment-correction-store.service';
import { WritingAssessmentItemState } from '../../models/writing.assessment.item.state.model';

@Component({
  selector: 'app-writing-list-result',
  templateUrl: './writing-list-result.component.html',
  styleUrls: ['./writing-list-result.component.scss'],
})
export class WritingListResultComponent implements OnInit {

  assessmentsStore = inject(AssessmentCorrectionStoreService);
  dataSource: WritingAssessmentItem[] = [];

  constructor() {
    effect(() => {
      if (this.assessmentsStore.assessments()) {
        console.log('WritingListResultComponent');

        this.dataSource = [...this.assessmentsStore.assessments()];

      }
    });
  }
  ngOnInit() { }

  getIconForState(state: WritingAssessmentItemState | undefined): string {
    if (state === undefined) {
      return 'help-circle-outline'; // Icono por defecto
    }
    switch (state) {
      case WritingAssessmentItemState.Pending:
        return 'hourglass-outline'; // Icono para estado "Pending"
      case WritingAssessmentItemState.Completed:
        return 'checkmark-circle-outline'; // Icono para estado "Completed"
      case WritingAssessmentItemState.Error:
        return 'close-circle-outline'; // Icono para estado "Error"
      case WritingAssessmentItemState.LimitReached:
        return 'alert-circle-outline'; // Icono para estado "Plan Limit Reached"
      default:
        return 'help-circle-outline'; // Icono por defecto
    }
  }

  // Método opcional para obtener el color dependiendo del estado
  getColorForState(state: WritingAssessmentItemState | undefined): string {
    if (state === undefined) {
      return 'medium'; // Color neutro por defecto
    }
    switch (state) {
      case WritingAssessmentItemState.Pending:
        return 'warning'; // Color amarillo para "Pending"
      case WritingAssessmentItemState.Completed:
        return 'success'; // Color verde para "Completed"
      case WritingAssessmentItemState.Error:
        return 'danger'; // Color rojo para "Error"
      case WritingAssessmentItemState.LimitReached:
        return 'tertiary'; // Color azul para "Plan Limit Reached"
      default:
        return 'medium'; // Color neutro por defecto
    }
  }

}
