import { NgModule } from '@angular/core';
import { UsersRoutingModule } from './users-routing.module';
import { ListUsersComponent } from './pages/list/list-users.component';
import { UserFormComponent } from './pages/form/user-form.component';
import { RegisterUserDialogComponent } from './pages/register/register-user-dialog.component';
import { UpdateUserDialogComponent } from './pages/update/update-user-dialog.component';
import { AuthModule } from '../../@core/auth/auth.module';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatIconModule } from '@angular/material/icon';
import { MatTableModule } from '@angular/material/table';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatDialogModule } from '@angular/material/dialog';
import { SharedModule } from '../../@shared/shared.module';
import { MatMenuModule } from '@angular/material/menu';
import { DeleteUserDialogComponent } from './pages/delete/delete-user-dialog.component';
import { MatPaginator } from '@angular/material/paginator';

@NgModule({
  imports: [
    AuthModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatInputModule,
    MatDialogModule,
    MatMenuModule,
    MatPaginator,
    MatSelectModule,
    MatTableModule,
    MatTooltipModule,
    UsersRoutingModule,
    SharedModule,
  ],
  declarations: [
    ListUsersComponent,
    DeleteUserDialogComponent,
    RegisterUserDialogComponent,
    UpdateUserDialogComponent,
    UserFormComponent,
  ],
})
export class UsersModule { }
