import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { User } from '../../models/user.model';
import { UserManagementService } from '../../services/user-management.service';

@Component({
    selector: 'hrt-update-user',
    templateUrl: './update-user-dialog.component.html',
    standalone: false
})
export class UpdateUserDialogComponent {
  constructor(
    private readonly service: UserManagementService,
    private readonly dialogRef: MatDialogRef<UpdateUserDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public user: User
  ) {}

  close(): void {
    this.dialogRef.close(false);
  }

  onSave(user: User): void {
    this.service.update(user).subscribe(() => this.dialogRef.close(true));
  }
}
