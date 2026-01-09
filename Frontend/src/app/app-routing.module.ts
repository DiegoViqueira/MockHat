import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';
import { AppRoutes } from './@core/auth/models/routes.enum';

const routes: Routes = [
  {
    path: AppRoutes.Modules,
    loadChildren: () => import('./modules/modules.module').then((m) => m.ModulesModule),
  },
  {
    path: 'auth',
    loadChildren: () => import('./@core/auth/auth.module').then((m) => m.AuthModule),
  },
  { path: '', redirectTo: AppRoutes.Modules, pathMatch: 'full' },
  { path: '**', redirectTo: AppRoutes.Modules, pathMatch: 'prefix' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { useHash: false })],
  exports: [RouterModule],
})
export class AppRoutingModule { }
