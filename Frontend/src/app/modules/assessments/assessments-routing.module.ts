import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AssessmentsComponent } from './assessments.component';
import { CreateAssessmentComponent } from './components/create-assessment/create-assessment.component';
import { AppRoutes } from '../../@core/auth/models/routes.enum';
import { AssessmentWritingDetailsComponent } from './components/assessment-writing-details/assessment-writing-details.component';
import { ViewAssessmentComponent } from './components/view-assessment/view-assessment.component';
const routes: Routes = [
  {
    path: '',
    component: AssessmentsComponent,
    children: [
      { path: AppRoutes.CreateAssessment, component: CreateAssessmentComponent },
      { path: `${AppRoutes.ViewAssessment}`, component: ViewAssessmentComponent },
      { path: `${AppRoutes.AssessmentWritingDetails}`, component: AssessmentWritingDetailsComponent },
      { path: '', redirectTo: '.', pathMatch: 'full' },
      { path: '**', redirectTo: '.' },
    ],
  },
  { path: '', redirectTo: '.', pathMatch: 'full' },
  { path: '**', redirectTo: '.' },

];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AssessmentsRoutingModule { }
