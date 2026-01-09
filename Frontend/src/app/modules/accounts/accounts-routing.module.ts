import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AccountsComponent } from './accounts.component';
import { AccountComponent } from './pages/account/account.component';
import { AppRoutes } from '../../@core/auth/models/routes.enum';
const routes: Routes = [
  {
    path: '',
    component: AccountsComponent,
    children: [
      {
        path: '',
        component: AccountComponent
      },
      { path: '', redirectTo: AppRoutes.Account, pathMatch: 'full' },
      { path: '**', redirectTo: AppRoutes.Account },
    ]
  },

  { path: '', redirectTo: AppRoutes.Account, pathMatch: 'full' },
  { path: '**', redirectTo: AppRoutes.Account },

];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AccountsRoutingModule { }
