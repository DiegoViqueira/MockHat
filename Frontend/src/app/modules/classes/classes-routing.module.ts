import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ClassItemComponent } from './pages/class-item/class-item.component';
import { AppRoutes } from '../../@core/auth/models/routes.enum';
import { ClassesComponent } from './classes.component';
import { ClassesManagementComponent } from './pages/classes/classes-management.component';
import { ClassMetricsComponent } from './pages/class-metrics/class-metrics.component';
import { ClassAnalisysComponent } from './components/class-analisys/class-analisys.component';

const routes: Routes = [
  {
    path: '',
    component: ClassesComponent,
    children: [
      {
        path: '',
        component: ClassesManagementComponent,
        //canMatch: [canMatchRoleGuard],
      },
      {
        path: AppRoutes.Class,
        component: ClassItemComponent,
        //canMatch: [canMatchRoleGuard],
      },
      {
        path: AppRoutes.ClassMetrics,
        component: ClassMetricsComponent,
        //canMatch: [canMatchRoleGuard],
      },
      {
        path: AppRoutes.ClassAnalysis,
        component: ClassAnalisysComponent,
        //canMatch: [canMatchRoleGuard],
      },
      { path: '', redirectTo: '.', pathMatch: 'full' }, // Assuming AppRoutes.Assessments is 'assessments'
      { path: '**', redirectTo: '.' }, // Assuming AppRoutes.Assessments is 'assessments'
    ],

  },
  { path: '', redirectTo: '.', pathMatch: 'full' },
  { path: '**', redirectTo: '.' },

];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ClassesRoutingModule { }
