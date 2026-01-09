import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { AccountsRoutingModule } from './accounts-routing.module';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';
import { MatMenuModule } from '@angular/material/menu';
import { MatDividerModule } from '@angular/material/divider';
import { MatListModule } from '@angular/material/list';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { SharedModule } from '../../@shared/shared.module';
import { ReactiveFormsModule } from '@angular/forms';
import { AccountsComponent } from './accounts.component';
import { AccountComponent } from './pages/account/account.component';
import { MatChipsModule } from '@angular/material/chips';
import { InviteUserComponent } from './components/invite-user/invite-user.component';
import { MatDialogModule } from '@angular/material/dialog';
import { MatTableModule } from '@angular/material/table';
import { MatTabsModule } from '@angular/material/tabs';
import { TranslateModule } from '@ngx-translate/core';
@NgModule({
  declarations: [AccountsComponent, AccountComponent, InviteUserComponent],
  imports: [
    CommonModule,
    AccountsRoutingModule,
    RouterModule,
    MatCardModule,
    MatIconModule,
    MatButtonModule,
    MatMenuModule,
    MatDividerModule,
    MatListModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    SharedModule,
    ReactiveFormsModule,
    MatChipsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatButtonModule,
    MatDialogModule,
    MatTableModule,
    MatTabsModule,
    TranslateModule,


  ],
  exports: [AccountsComponent, AccountComponent, InviteUserComponent]
})
export class AccountsModule { }
