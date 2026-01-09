import { Component, inject, OnChanges } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { levels } from '../../../@shared/common-environment/common-environment';
import { User } from '../../users/models/user.model';

@Component({
  selector: 'wlk-student-dialog',
  templateUrl: './student-dialog.component.html',
  styleUrl: './student-dialog.component.scss',
  standalone: false
})
export class StudentDialogComponent implements OnChanges {
  data = inject(MAT_DIALOG_DATA);
  studentForm!: FormGroup;

  constructor(
    private fb: FormBuilder,
    private readonly dialogRef: MatDialogRef<StudentDialogComponent>
  ) {
    this.studentForm = this.fb.group({
      _id: [''],
      name: ['', Validators.required],
      account_id: [''],
      last_name: ['', Validators.required],
      email: [''],
      active: [true],
      created_at: [new Date(), Validators.required],
      updated_at: [new Date(), Validators.required],
    });

    if (this.data.student) {
      this.studentForm.setValue(this.data.student);
    }
  }

  ngOnChanges(): void {
    if (this.data !== null) {
      this.studentForm.setValue(this.data.student);
    }
  }

  protected readonly levels = levels;
  onSubmit() {
    if (this.studentForm.valid) {
      this.dialogRef.close(this.studentForm.getRawValue());
    }
  }

  close(): void {
    this.dialogRef.close(false);
  }
}
