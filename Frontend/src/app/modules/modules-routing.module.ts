import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AppRoutes } from '../@core/auth/models/routes.enum';
import { ModulesComponent } from './modules.component';
import { canActivateAuthGuard } from '../@core/auth/guards/canActivateAuth.guard';

const routes: Routes = [
  {
    path: '',
    component: ModulesComponent,
    canActivate: [canActivateAuthGuard],
    children: [

      {
        path: AppRoutes.Account,
        canActivate: [canActivateAuthGuard],
        loadChildren: () => import('./accounts/accounts-routing.module').then((m) => m.AccountsRoutingModule),
      },
      // {
      //   path: AppRoutes.Home,
      //   canActivate: [canActivateAuthGuard],
      //   loadChildren: () => import('./home/home/home-routing.module').then((m) => m.HomeRoutingModule),
      // },

      {
        path: AppRoutes.Classes,
        canActivate: [canActivateAuthGuard],
        loadChildren: () => import('./classes/classes.module').then((m) => m.ClassesModule),
        //canMatch: [canMatchRoleGuard],
      },
      {
        path: AppRoutes.Students,
        canActivate: [canActivateAuthGuard],
        loadChildren: () => import('./students/students.module').then((m) => m.StudentsModule),
        //canMatch: [canMatchRoleGuard],
      },
      {
        path: AppRoutes.Assessments,
        canActivate: [canActivateAuthGuard],
        loadChildren: () => import('./assessments/assessments.module').then((m) => m.AssessmentsModule),
        //canMatch: [canMatchRoleGuard],
      },
      {
        path: AppRoutes.Users,
        //canActivate: [canActivateAuthGuard],
        loadChildren: () =>
          import('./users/users-routing.module').then((m) => m.UsersRoutingModule),
        //canMatch: [canMatchRoleGuard],
      },
      {
        path: AppRoutes.Billing,
        //canActivate: [canActivateAuthGuard],
        loadChildren: () =>
          import('./plans/plans-routing.module').then((m) => m.PlansRoutingModule),
        //canMatch: [canMatchRoleGuard],
      },

      { path: '', redirectTo: AppRoutes.Classes, pathMatch: 'full' },
      { path: '**', redirectTo: AppRoutes.Classes },
    ],
  },
  { path: '', redirectTo: AppRoutes.Classes, pathMatch: 'full' },
  { path: '**', redirectTo: AppRoutes.Classes },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class ModulesRoutingModule { }
