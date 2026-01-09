import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ModulesComponent } from './modules.component';
import { WirtingPage } from './pages/wirting/wirting.page';
import { GrammarPage } from './pages/grammar/grammar.page';
import { canActivateAuthGuard } from '../@core/auth/guards/canActivateAuth.guard';

const routes: Routes = [
  {
    path: '',
    component: ModulesComponent,
    children: [
      {
        path: 'writing',
        component: WirtingPage, // Ruta interna para el dashboard
        canActivate: [canActivateAuthGuard],
      },
      {
        path: 'grammar',
        component: GrammarPage, // Ruta interna para el dashboard
        canActivate: [canActivateAuthGuard],
      },
      {
        path: '',
        redirectTo: 'writing',
        pathMatch: 'full',
      },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ModulesRoutingModule { }
