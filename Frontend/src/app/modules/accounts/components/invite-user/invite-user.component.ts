import { Component, inject, OnInit } from '@angular/core';
import { FormControl, Validators, FormBuilder, FormGroup } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { Role } from '../../../../@core/auth/models/role.enum';

@Component({
  selector: 'wlk-invite-user',
  templateUrl: './invite-user.component.html',
  styleUrl: './invite-user.component.scss',
  standalone: false
})
export class InviteUserComponent implements OnInit {
  dialogRef = inject(MatDialogRef);

  _fb = inject(FormBuilder);

  roles = [Role.ADMIN, Role.MEMBER];

  form: FormGroup;


  ngOnInit(): void {
    this.form = this._fb.group({
      email: ['', [Validators.required, Validators.email]],
      role: [Role.MEMBER, [Validators.required]]
    });
  }

  onSubmit() {
    this.dialogRef.close(this.form.getRawValue());
  }

  closeDialog() {
    this.dialogRef.close();
  }


}
