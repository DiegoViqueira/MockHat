import { Component, computed, effect, inject } from '@angular/core';
import { AssessmentStore } from '../../../assessments/stores/assessment.store';
import { Assessment } from '../../../assessments/models/assessment.model';
import { MatTableDataSource } from '@angular/material/table';
import { DeviceDetectionService } from '../../../../@core/services/device-detection.service';
import { AppRoutes } from '../../../../@core/auth/models/routes.enum';
import { Router } from '@angular/router';
import { WritingState } from '../../../assessments/models/writing.state.model';
import { AssessmentState } from '../../../assessments/models/assessment.state.model';
@Component({
  selector: 'wlk-class-assessments-table',
  templateUrl: './class-assessments-table.component.html',
  styleUrl: './class-assessments-table.component.scss',
  standalone: false
})
export class ClassAssessmentsTableComponent {

  router = inject(Router);
  assessmentStore = inject(AssessmentStore);
  assessments = computed(() => this.assessmentStore.assessments());
  dataSource = new MatTableDataSource<Assessment>([]);

  device = inject(DeviceDetectionService);
  isMobile = this.device.isMobileScreen;

  constructor() {
    effect(() => {
      this.dataSource.data = this.assessments();
    });
  }


  getIconForState(state: AssessmentState) {
    switch (state) {
      case AssessmentState.PENDING:
        return 'schedule';
      case AssessmentState.COMPLETED:
        return 'check_circle';
      case AssessmentState.STARTED:
        return 'play_arrow';
      case AssessmentState.ERROR:
        return 'error';
    }
  }

  // Definir las columnas que se mostrarán
  displayedColumns: string[] = ['title', 'state', 'actions'];



  navigateToViewAssessment(assessment: Assessment) {
    this.assessmentStore.setAssessment(assessment);
    this.router.navigate([AppRoutes.Modules, AppRoutes.Assessments, AppRoutes.ViewAssessment],
      {
        queryParams: { mode: 'view' }
      }
    );
  }


  navigateToAddMoreWritings(assessment: Assessment) {
    this.assessmentStore.setAssessment(assessment);
    this.router.navigate([AppRoutes.Modules, AppRoutes.Assessments, AppRoutes.ViewAssessment],
      {
        queryParams: { mode: 'add_more_writings' }
      }
    );
  }

  navigateToCorrectAssessment(assessment: Assessment) {
    this.assessmentStore.setAssessment(assessment);
    this.router.navigate([AppRoutes.Modules, AppRoutes.Assessments, AppRoutes.ViewAssessment],
      {
        queryParams: { mode: 'correct' }
      }
    );
  }

  navigateToCreateAssessment() {
    this.router.navigate([AppRoutes.Modules, AppRoutes.Assessments, AppRoutes.CreateAssessment]);
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }


}
