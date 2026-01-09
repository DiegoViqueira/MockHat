import { Component, inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
@Component({
  selector: 'hrt-delete-template',
  templateUrl: './delete-template.component.html',
  styleUrl: './delete-template.component.scss',
  standalone: false
})
export class DeleteTemplateComponent {

  data: {
    title: string;
    message: string;
  }

  DIALOG_DATA = inject(MAT_DIALOG_DATA);
  dialogRef: MatDialogRef<DeleteTemplateComponent>;

  constructor() {
    this.data = this.DIALOG_DATA;
    this.dialogRef = inject(MatDialogRef<DeleteTemplateComponent>);
  }

  onCancel() {
    this.dialogRef.close(false);
  }

  onConfirm() {
    this.dialogRef.close(true);
  }
}
