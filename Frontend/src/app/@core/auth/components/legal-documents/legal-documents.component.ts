import { Component, inject } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'wlk-legal-documents',
  templateUrl: './legal-documents.component.html',
  styleUrl: './legal-documents.component.scss',
  standalone: false
})
export class LegalDocumentsComponent {

  private dialogRef = inject(MatDialogRef);
  private data = inject(MAT_DIALOG_DATA);



  onCancel() {
    this.dialogRef.close();
  }
}
