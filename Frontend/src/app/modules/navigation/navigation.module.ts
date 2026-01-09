import { NgModule } from '@angular/core';
import { NavigationComponent } from './pages/navigation/navigation.component';
import { MatIconModule } from '@angular/material/icon';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatButtonModule } from '@angular/material/button';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatListModule } from '@angular/material/list';
import { RouterModule } from '@angular/router';
import { MatMenuModule } from '@angular/material/menu';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatBadgeModule } from '@angular/material/badge';
import { SharedModule } from '../../@shared/shared.module';
import { HeaderComponent } from './pages/header/header.component';
import { ToolbarComponent } from './pages/toolbar/toolbar.component';

@NgModule({
  declarations: [HeaderComponent, NavigationComponent, ToolbarComponent],
  imports: [
    RouterModule,
    MatBadgeModule,
    MatButtonModule,
    MatIconModule,
    MatListModule,
    MatMenuModule,
    MatSidenavModule,
    MatToolbarModule,
    MatTooltipModule,
    SharedModule,

  ],
  exports: [HeaderComponent, NavigationComponent, ToolbarComponent],
})
export class NavigationModule { }
