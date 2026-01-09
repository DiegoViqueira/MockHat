import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { User } from '../../models/user.model';
import { UserManagementService } from '../../services/user-management.service';

@Component({
    selector: 'hrt-delete-user',
    templateUrl: './delete-user-dialog.component.html',
    standalone: false
})
export class DeleteUserDialogComponent {
  constructor(
    private readonly service: UserManagementService,
    private readonly dialogRef: MatDialogRef<DeleteUserDialogComponent>,
    @Inject(MAT_DIALOG_DATA) private readonly user: User
  ) { }

  onCancel(): void {
    this.dialogRef.close(false);
  }

  onDelete(): void {
  }
}
