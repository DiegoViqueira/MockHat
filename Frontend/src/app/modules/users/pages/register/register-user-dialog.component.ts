import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { User } from '../../models/user.model';
import { UserManagementService } from '../../services/user-management.service';

@Component({
    selector: 'hrt-register-user',
    templateUrl: './register-user-dialog.component.html',
    standalone: false
})
export class RegisterUserDialogComponent {
  constructor(
    private readonly service: UserManagementService,
    private readonly dialogRef: MatDialogRef<RegisterUserDialogComponent>
  ) { }

  close(): void {
    this.dialogRef.close(false);
  }

  onSave(user: User): void {
    this.service
      .register(user)
      .pipe()
      .subscribe(() => this.dialogRef.close(true));
  }
}
