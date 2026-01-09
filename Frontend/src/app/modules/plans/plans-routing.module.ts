import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AppRoutes } from '../../@core/auth/models/routes.enum';
import { PlansComponent } from './plans.component';
import { PlanInfoComponent } from './pages/plan-info/plan-info.component';

const routes: Routes = [
  {
    path: '',
    component: PlansComponent,
    children: [
      {
        path: AppRoutes.Billing,
        component: PlanInfoComponent,
        //canMatch: [canMatchRoleGuard],
      },
      { path: '', redirectTo: AppRoutes.Billing, pathMatch: 'full' },
      { path: '**', redirectTo: AppRoutes.Billing },
    ],
  },
  { path: '', redirectTo: AppRoutes.Billing, pathMatch: 'full' },
  { path: '**', redirectTo: AppRoutes.Billing },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class PlansRoutingModule { }
