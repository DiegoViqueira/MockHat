import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { AssessmentsRoutingModule } from './assessments-routing.module';
import { AssessmentsComponent } from './assessments.component';
import { CreateAssessmentComponent } from './components/create-assessment/create-assessment.component';
import { SharedModule } from '../../@shared/shared.module';
import { TranslateModule } from '@ngx-translate/core';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatChipsModule } from '@angular/material/chips';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatDialogModule } from '@angular/material/dialog';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { MatTableModule } from '@angular/material/table';
import { AssessmentWritingViewComponent } from './components/assessment-writing-view/assessment-writing-view.component';
import { AssessmentWritingCorrectComponent } from './components/assessment-writing-correct/assessment-writing-correct.component';
import { AssessmentWritingDetailsComponent } from './components/assessment-writing-details/assessment-writing-details.component';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatListModule } from '@angular/material/list';
import { ViewAssessmentComponent } from './components/view-assessment/view-assessment.component';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatMenuModule } from '@angular/material/menu';
@NgModule({
  declarations: [AssessmentsComponent, CreateAssessmentComponent, ViewAssessmentComponent,
    AssessmentWritingViewComponent, AssessmentWritingCorrectComponent, AssessmentWritingDetailsComponent],
  imports: [
    CommonModule,
    AssessmentsRoutingModule,
    RouterModule,
    TranslateModule,
    SharedModule,
    MatIconModule,
    MatButtonModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatDialogModule,
    MatChipsModule,
    MatTooltipModule,
    MatProgressSpinnerModule,
    ReactiveFormsModule,
    MatTableModule,
    MatTooltipModule,
    MatSidenavModule,
    MatToolbarModule,
    MatListModule,
    FormsModule,
    MatExpansionModule,
    MatMenuModule
  ]
})
export class AssessmentsModule { }
