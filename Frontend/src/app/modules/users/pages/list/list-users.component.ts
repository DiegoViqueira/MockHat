import { Component, effect, inject, ViewChild } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { User } from '../../models/user.model';
import { UserManagementService } from '../../services/user-management.service';
import { RegisterUserDialogComponent } from '../register/register-user-dialog.component';
import { UpdateUserDialogComponent } from '../update/update-user-dialog.component';
import { DeleteUserDialogComponent } from '../delete/delete-user-dialog.component';
import {
  dialogConfigFactory,
  tablePageSizes,
} from '../../../../@shared/common-environment/common-environment';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { UserStore } from '../../stores/user.store';

@Component({
    selector: 'hrt-list-users',
    templateUrl: './list-users.component.html',
    standalone: false
})
export class ListUsersComponent {
  displayedColumns: string[] = [
    'first_name',
    'last_name',
    'email',
    'role',
    'verified',
    'disabled',
    'created_at',
    'Actions',
  ];


  store = inject(UserStore);
  pageSize = tablePageSizes;
  dataSource: MatTableDataSource<User> = new MatTableDataSource<User>([]);
  @ViewChild(MatPaginator, { static: true }) paginator: MatPaginator;

  constructor(
    private readonly service: UserManagementService,
    public dialog: MatDialog
  ) {
    effect(() => {
      this.dataSource.data = this.store.users();
      this.dataSource.paginator = this.paginator;
    });
  }

  onRegister() {
    this.dialog
      .open(RegisterUserDialogComponent, dialogConfigFactory({ width: '30%' }))
      .afterClosed()
      .subscribe();
  }

  onUpdate(user: User) {
    const config = dialogConfigFactory({ data: user, width: '30%' });
    this.dialog.open(UpdateUserDialogComponent, config).afterClosed().subscribe();
  }

  onRemove(user: User) {
    const config = dialogConfigFactory({ data: user, width: '30%' });
    this.dialog.open(DeleteUserDialogComponent, config).afterClosed().subscribe();
  }
}
